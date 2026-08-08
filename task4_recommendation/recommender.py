#!/usr/bin/env python3
"""
Task 4: Recommendation System
A recommendation system using collaborative filtering and content-based filtering.
Supports movie, book, and product recommendations.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import json
import random
from math import sqrt


class FilterType(Enum):
    COLLABORATIVE = "collaborative"
    CONTENT_BASED = "content_based"
    HYBRID = "hybrid"


@dataclass
class Item:
    """Represents an item (movie, book, product)."""
    id: str
    name: str
    category: str
    features: Dict[str, float]  # For content-based filtering
    metadata: Dict = None


@dataclass
class Rating:
    """User-item rating."""
    user_id: str
    item_id: str
    rating: float
    timestamp: int = 0


class CollaborativeFiltering:
    """User-based and Item-based Collaborative Filtering."""
    
    def __init__(self, k_neighbors: int = 5, min_common: int = 2):
        self.k_neighbors = k_neighbors
        self.min_common = min_common
        self.user_item_matrix: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.item_user_matrix: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.user_similarities: Dict[str, Dict[str, float]] = {}
        self.item_similarities: Dict[str, Dict[str, float]] = {}
        self.user_means: Dict[str, float] = {}
        self.item_means: Dict[str, float] = {}
    
    def fit(self, ratings: List[Rating]):
        """Build user-item and item-user matrices."""
        for r in ratings:
            self.user_item_matrix[r.user_id][r.item_id] = r.rating
            self.item_user_matrix[r.item_id][r.user_id] = r.rating
        
        # Compute user means
        for user, items in self.user_item_matrix.items():
            self.user_means[user] = np.mean(list(items.values()))
        
        # Compute item means
        for item, users in self.item_user_matrix.items():
            self.item_means[item] = np.mean(list(users.values()))
        
        # Compute similarities
        self._compute_user_similarities()
        self._compute_item_similarities()
    
    def _pearson_correlation(self, user1: str, user2: str) -> float:
        """Compute Pearson correlation between two users."""
        items1 = self.user_item_matrix[user1]
        items2 = self.user_item_matrix[user2]
        common_items = set(items1.keys()) & set(items2.keys())
        
        if len(common_items) < self.min_common:
            return 0.0
        
        # Center ratings by user mean
        mean1 = self.user_means[user1]
        mean2 = self.user_means[user2]
        
        num = sum((items1[i] - mean1) * (items2[i] - mean2) for i in common_items)
        den1 = sqrt(sum((items1[i] - mean1) ** 2 for i in common_items))
        den2 = sqrt(sum((items2[i] - mean2) ** 2 for i in common_items))
        
        if den1 == 0 or den2 == 0:
            return 0.0
        
        return num / (den1 * den2)
    
    def _compute_user_similarities(self):
        """Compute user-user similarities."""
        users = list(self.user_item_matrix.keys())
        for i, u1 in enumerate(users):
            self.user_similarities[u1] = {}
            for u2 in users[i+1:]:
                sim = self._pearson_correlation(u1, u2)
                if sim > 0:
                    self.user_similarities[u1][u2] = sim
                    if u2 not in self.user_similarities:
                        self.user_similarities[u2] = {}
                    self.user_similarities[u2][u1] = sim
    
    def _compute_item_similarities(self):
        """Compute item-item similarities."""
        items = list(self.item_user_matrix.keys())
        for i, item1 in enumerate(items):
            self.item_similarities[item1] = {}
            for item2 in items[i+1:]:
                sim = self._pearson_correlation_items(item1, item2)
                if sim > 0:
                    self.item_similarities[item1][item2] = sim
                    if item2 not in self.item_similarities:
                        self.item_similarities[item2] = {}
                    self.item_similarities[item2][item1] = sim
    
    def _pearson_correlation_items(self, item1: str, item2: str) -> float:
        """Pearson correlation for items."""
        users1 = self.item_user_matrix[item1]
        users2 = self.item_user_matrix[item2]
        common_users = set(users1.keys()) & set(users2.keys())
        
        if len(common_users) < self.min_common:
            return 0.0
        
        mean1 = self.item_means[item1]
        mean2 = self.item_means[item2]
        
        num = sum((users1[u] - mean1) * (users2[u] - mean2) for u in common_users)
        den1 = sqrt(sum((users1[u] - mean1) ** 2 for u in common_users))
        den2 = sqrt(sum((users2[u] - mean2) ** 2 for u in common_users))
        
        if den1 == 0 or den2 == 0:
            return 0.0
        
        return num / (den1 * den2)
    
    def predict_user_based(self, user_id: str, item_id: str) -> float:
        """Predict rating using user-based CF."""
        if user_id not in self.user_item_matrix:
            return self.item_means.get(item_id, 3.0)
        
        if item_id not in self.item_user_matrix:
            return self.user_means.get(user_id, 3.0)
        
        # Find similar users who rated this item
        similar_users = []
        for sim_user, sim in self.user_similarities.get(user_id, {}).items():
            if item_id in self.user_item_matrix[sim_user]:
                similar_users.append((sim_user, sim))
        
        if not similar_users:
            return self.user_means.get(user_id, 3.0)
        
        # Take top-k
        similar_users.sort(key=lambda x: x[1], reverse=True)
        top_k = similar_users[:self.k_neighbors]
        
        # Weighted average
        user_mean = self.user_means[user_id]
        num = sum(sim * (self.user_item_matrix[u][item_id] - self.user_means[u]) 
                  for u, sim in top_k)
        den = sum(abs(sim) for _, sim in top_k)
        
        if den == 0:
            return user_mean
        
        return user_mean + num / den
    
    def predict_item_based(self, user_id: str, item_id: str) -> float:
        """Predict rating using item-based CF."""
        if user_id not in self.user_item_matrix:
            return self.item_means.get(item_id, 3.0)
        
        if item_id not in self.item_user_matrix:
            return self.user_means.get(user_id, 3.0)
        
        user_ratings = self.user_item_matrix[user_id]
        similar_items = []
        
        for rated_item, rating in user_ratings.items():
            if rated_item in self.item_similarities:
                for sim_item, sim in self.item_similarities[rated_item].items():
                    if sim_item == item_id:
                        similar_items.append((sim, rating))
        
        if not similar_items:
            return self.user_means.get(user_id, 3.0)
        
        similar_items.sort(key=lambda x: x[0], reverse=True)
        top_k = similar_items[:self.k_neighbors]
        
        num = sum(sim * rating for sim, rating in top_k)
        den = sum(abs(sim) for sim, _ in top_k)
        
        if den == 0:
            return self.user_means.get(user_id, 3.0)
        
        return num / den
    
    def recommend(self, user_id: str, n: int = 5, method: str = "item") -> List[Tuple[str, float]]:
        """Get top-N recommendations for user."""
        if user_id not in self.user_item_matrix:
            return []
        
        rated_items = set(self.user_item_matrix[user_id].keys())
        all_items = set(self.item_user_matrix.keys())
        unrated = all_items - rated_items
        
        predictions = []
        for item in unrated:
            if method == "user":
                pred = self.predict_user_based(user_id, item)
            else:
                pred = self.predict_item_based(user_id, item)
            predictions.append((item, pred))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n]


class ContentBasedFiltering:
    """Content-based filtering using item features."""
    
    def __init__(self):
        self.items: Dict[str, Item] = {}
        self.item_profiles: Dict[str, np.ndarray] = {}
        self.feature_names: List[str] = []
        self.user_profiles: Dict[str, np.ndarray] = {}
    
    def add_item(self, item: Item):
        """Add item to the system."""
        self.items[item.id] = item
    
    def fit(self, ratings: List[Rating]):
        """Build item profiles and user profiles."""
        # Get all feature names
        all_features = set()
        for item in self.items.values():
            all_features.update(item.features.keys())
        self.feature_names = sorted(list(all_features))
        
        # Build item profiles
        for item_id, item in self.items.items():
            profile = np.array([item.features.get(f, 0.0) for f in self.feature_names])
            # Normalize
            norm = np.linalg.norm(profile)
            if norm > 0:
                profile = profile / norm
            self.item_profiles[item_id] = profile
        
        # Build user profiles from ratings
        user_features = defaultdict(lambda: np.zeros(len(self.feature_names)))
        user_counts = defaultdict(int)
        
        for r in ratings:
            if r.item_id in self.item_profiles:
                user_features[r.user_id] += self.item_profiles[r.item_id] * r.rating
                user_counts[r.user_id] += 1
        
        for user_id, features in user_features.items():
            if user_counts[user_id] > 0:
                profile = features / user_counts[user_id]
                norm = np.linalg.norm(profile)
                if norm > 0:
                    profile = profile / norm
                self.user_profiles[user_id] = profile
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity."""
        return np.dot(vec1, vec2)
    
    def predict(self, user_id: str, item_id: str) -> float:
        """Predict rating based on content similarity."""
        if user_id not in self.user_profiles or item_id not in self.item_profiles:
            return 3.0
        
        sim = self.cosine_similarity(self.user_profiles[user_id], self.item_profiles[item_id])
        # Convert similarity to rating scale (1-5)
        return 1 + 4 * (sim + 1) / 2
    
    def recommend(self, user_id: str, n: int = 5) -> List[Tuple[str, float]]:
        """Get top-N content-based recommendations."""
        if user_id not in self.user_profiles:
            return []
        
        rated_items = set()
        # We'd need access to user's rated items - simplified here
        all_items = set(self.item_profiles.keys())
        
        predictions = []
        for item_id in all_items:
            pred = self.predict(user_id, item_id)
            predictions.append((item_id, pred))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:n]


class HybridRecommender:
    """Hybrid recommender combining collaborative and content-based."""
    
    def __init__(self, cf_weight: float = 0.6, cb_weight: float = 0.4):
        self.cf = CollaborativeFiltering()
        self.cb = ContentBasedFiltering()
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight
    
    def fit(self, ratings: List[Rating], items: Dict[str, Item]):
        """Fit both models."""
        for item in items.values():
            self.cb.add_item(item)
        self.cf.fit(ratings)
        self.cb.fit(ratings)
    
    def predict(self, user_id: str, item_id: str) -> float:
        """Hybrid prediction."""
        cf_pred = self.cf.predict_item_based(user_id, item_id)
        cb_pred = self.cb.predict(user_id, item_id)
        return self.cf_weight * cf_pred + self.cb_weight * cb_pred
    
    def recommend(self, user_id: str, n: int = 5, filter_type: FilterType = FilterType.HYBRID) -> List[Tuple[str, float]]:
        """Get recommendations."""
        if filter_type == FilterType.COLLABORATIVE:
            return self.cf.recommend(user_id, n, "item")
        elif filter_type == FilterType.CONTENT_BASED:
            return self.cb.recommend(user_id, n)
        else:
            # Hybrid
            rated = set(self.cf.user_item_matrix.get(user_id, {}).keys())
            all_items = set(self.cf.item_user_matrix.keys())
            unrated = all_items - rated
            
            predictions = []
            for item in unrated:
                pred = self.predict(user_id, item)
                predictions.append((item, pred))
            
            predictions.sort(key=lambda x: x[1], reverse=True)
            return predictions[:n]


def create_sample_data() -> Tuple[List[Rating], Dict[str, Item]]:
    """Create sample movie data for demonstration."""
    # Sample movies with features
    movies = {
        "m1": Item("m1", "The Matrix", "Sci-Fi", 
                   {"action": 0.9, "sci_fi": 0.9, "philosophy": 0.8, "romance": 0.1}),
        "m2": Item("m2", "Inception", "Sci-Fi",
                   {"action": 0.8, "sci_fi": 0.9, "thriller": 0.8, "romance": 0.2}),
        "m3": Item("m3", "The Dark Knight", "Action",
                   {"action": 0.9, "crime": 0.8, "drama": 0.7, "romance": 0.1}),
        "m4": Item("m4", "Pulp Fiction", "Crime",
                   {"crime": 0.9, "drama": 0.8, "dialogue": 0.9, "romance": 0.1}),
        "m5": Item("m5", "Forrest Gump", "Drama",
                   {"drama": 0.9, "romance": 0.6, "history": 0.7, "comedy": 0.3}),
        "m6": Item("m6", "The Shawshank Redemption", "Drama",
                   {"drama": 0.9, "hope": 0.9, "friendship": 0.8, "crime": 0.3}),
        "m7": Item("m7", "Interstellar", "Sci-Fi",
                   {"sci_fi": 0.9, "drama": 0.8, "space": 0.9, "family": 0.6}),
        "m8": Item("m8", "The Godfather", "Crime",
                   {"crime": 0.9, "drama": 0.9, "family": 0.8, "power": 0.9}),
        "m9": Item("m9", "Fight Club", "Drama",
                   {"drama": 0.8, "psychology": 0.9, "action": 0.5, "philosophy": 0.8}),
        "m10": Item("m10", "Good Will Hunting", "Drama",
                    {"drama": 0.9, "math": 0.7, "friendship": 0.8, "romance": 0.4}),
    }
    
    # Sample ratings from different users
    np.random.seed(42)
    users = [f"u{i}" for i in range(1, 11)]
    ratings = []
    
    # User preferences (some users like sci-fi, some like drama, etc.)
    user_prefs = {
        "u1": {"Sci-Fi": 0.9, "Action": 0.7},
        "u2": {"Drama": 0.9, "Crime": 0.6},
        "u3": {"Sci-Fi": 0.8, "Drama": 0.7},
        "u4": {"Crime": 0.8, "Drama": 0.7},
        "u5": {"Drama": 0.9, "Romance": 0.6},
        "u6": {"Drama": 0.8, "Action": 0.5},
        "u7": {"Sci-Fi": 0.9, "Drama": 0.8},
        "u8": {"Crime": 0.9, "Drama": 0.8},
        "u9": {"Drama": 0.8, "Psychology": 0.7},
        "u10": {"Drama": 0.8, "Math": 0.7},
    }
    
    for user in users:
        prefs = user_prefs[user]
        for movie_id, movie in movies.items():
            # Base rating from genre match
            score = 3.0
            for genre, weight in prefs.items():
                if genre.lower() in movie.features:
                    score += weight * movie.features[genre.lower()] * 2
            
            # Add noise
            score += np.random.normal(0, 0.5)
            score = max(1, min(5, score))
            
            # Only add rating with some probability (sparse matrix)
            if np.random.random() < 0.7:
                ratings.append(Rating(user, movie_id, round(score, 1)))
    
    return ratings, movies


def evaluate_model(recommender: HybridRecommender, test_ratings: List[Rating], k: int = 5) -> Dict:
    """Evaluate recommendation quality."""
    # Group test ratings by user
    user_test = defaultdict(list)
    for r in test_ratings:
        user_test[r.user_id].append((r.item_id, r.rating))
    
    metrics = {"precision": [], "recall": [], "rmse": []}
    
    for user_id, test_items in user_test.items():
        if user_id not in recommender.cf.user_item_matrix:
            continue
        
        # Get recommendations
        recs = recommender.recommend(user_id, k, FilterType.HYBRID)
        rec_items = set(item for item, _ in recs)
        test_item_ids = set(item for item, _ in test_items)
        
        # Precision & Recall
        hits = len(rec_items & test_item_ids)
        precision = hits / k if k > 0 else 0
        recall = hits / len(test_item_ids) if test_item_ids else 0
        
        metrics["precision"].append(precision)
        metrics["recall"].append(recall)
        
        # RMSE on test items
        for item_id, true_rating in test_items:
            pred = recommender.predict(user_id, item_id)
            metrics["rmse"].append((pred - true_rating) ** 2)
    
    return {
        "precision@k": np.mean(metrics["precision"]) if metrics["precision"] else 0,
        "recall@k": np.mean(metrics["recall"]) if metrics["recall"] else 0,
        "rmse": sqrt(np.mean(metrics["rmse"])) if metrics["rmse"] else 0
    }


def demo():
    """Run demonstration of the recommendation system."""
    print("=" * 60)
    print("RECOMMENDATION SYSTEM DEMO")
    print("=" * 60)
    
    # Create sample data
    ratings, movies = create_sample_data()
    print(f"\nLoaded {len(ratings)} ratings from {len(set(r.user_id for r in ratings))} users")
    print(f"Catalog: {len(movies)} movies")
    
    # Train hybrid recommender
    recommender = HybridRecommender(cf_weight=0.6, cb_weight=0.4)
    recommender.fit(ratings, movies)
    
    # Show recommendations for a few users
    test_users = ["u1", "u2", "u3", "u7"]
    
    for user_id in test_users:
        print(f"\n{'='*40}")
        print(f"Recommendations for {user_id}:")
        print(f"{'='*40}")
        
        # Show user's history
        user_ratings = recommender.cf.user_item_matrix.get(user_id, {})
        print(f"\nUser's ratings ({len(user_ratings)} movies):")
        for item_id, rating in sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {movies[item_id].name}: {rating}/5")
        
        # Collaborative filtering
        cf_recs = recommender.recommend(user_id, 5, FilterType.COLLABORATIVE)
        print(f"\nCollaborative Filtering:")
        for item_id, score in cf_recs:
            print(f"  {movies[item_id].name}: {score:.2f}")
        
        # Content-based
        cb_recs = recommender.recommend(user_id, 5, FilterType.CONTENT_BASED)
        print(f"\nContent-Based Filtering:")
        for item_id, score in cb_recs:
            print(f"  {movies[item_id].name}: {score:.2f}")
        
        # Hybrid
        hybrid_recs = recommender.recommend(user_id, 5, FilterType.HYBRID)
        print(f"\nHybrid (CF + CB):")
        for item_id, score in hybrid_recs:
            print(f"  {movies[item_id].name}: {score:.2f}")
    
    # Evaluate
    print(f"\n{'='*40}")
    print("EVALUATION (on training data):")
    print(f"{'='*40}")
    metrics = evaluate_model(recommender, ratings, k=5)
    print(f"Precision@5: {metrics['precision@k']:.3f}")
    print(f"Recall@5:    {metrics['recall@k']:.3f}")
    print(f"RMSE:        {metrics['rmse']:.3f}")
    
    print(f"\n{'='*60}")
    print("Demo complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        demo()