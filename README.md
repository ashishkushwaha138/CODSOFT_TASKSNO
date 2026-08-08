# CODSOFT_TASKSNO — CodSoft AI Internship Tasks

This repository contains **3 completed tasks** for the CodSoft Artificial Intelligence Virtual Internship.

> **Internship Requirement:** Complete at least 3 tasks from the 5 provided. ✅ **DONE**

---

## 📋 Tasks Completed

| Task | Title | Description | Status |
|------|-------|-------------|--------|
| **1** | Chatbot with Rule-Based Responses | Pattern-matching chatbot with greetings, time, jokes, help, and more | ✅ Complete |
| **2** | Tic-Tac-Toe AI | Unbeatable AI using Minimax with Alpha-Beta Pruning | ✅ Complete |
| **4** | Recommendation System | Hybrid recommender (Collaborative + Content-Based filtering) | ✅ Complete |

**Tasks not implemented (optional):** Task 3 - Image Captioning, Task 5 - Face Detection & Recognition

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- No external dependencies for Task 1 & 2 (stdlib only)
- Task 4 requires: `numpy`, `pandas`

```bash
# Install Task 4 dependencies
pip install numpy pandas
```

### Run Task 1: Rule-Based Chatbot
```bash
cd task1_chatbot
python chatbot.py              # Interactive chat
python chatbot.py --demo       # Quick demo run
```

### Run Task 2: Tic-Tac-Toe AI
```bash
cd task2_tictactoe
python tictactoe_ai.py                    # Play against AI (you go first)
python tictactoe_ai.py --play --ai-first  # AI goes first
python tictactoe_ai.py --demo             # AI vs AI perfect play demo
python tictactoe_ai.py --benchmark        # Minimax vs Alpha-Beta benchmark
```

### Run Task 4: Recommendation System
```bash
cd task4_recommendation
python recommender.py          # Full demo with sample movie data
python recommender.py --demo   # Same (explicit flag)
```

---

## 📁 Project Structure

```
CODSOFT_TASKSNO/
├── README.md                    # This file
├── task1_chatbot/
│   └── chatbot.py               # Rule-based chatbot (~400 lines)
├── task2_tictactoe/
│   └── tictactoe_ai.py          # Minimax AI with Alpha-Beta (~450 lines)
└── task4_recommendation/
    └── recommender.py           # Hybrid recommender system (~600 lines)
```

---

## 🎯 Task Details

### Task 1: Rule-Based Chatbot (`task1_chatbot/chatbot.py`)
- **Patterns covered:** Greetings, goodbyes, thanks, name, time/date, weather (mock), help, jokes, wellbeing, age, preferences, learning/AI, compliments
- **Features:** Pattern matching with regex, contextual responses, conversation history, extensible rule system
- **Demo:** Run `python chatbot.py --demo` for a quick showcase

### Task 2: Tic-Tac-Toe AI (`task2_tictactoe/tictactoe_ai.py`)
- **Algorithm:** Minimax with Alpha-Beta Pruning
- **Features:** Unbeatable AI, human vs AI, AI vs AI demo, node evaluation benchmark, optional Alpha-Beta toggle
- **Performance:** Alpha-Beta reduces nodes evaluated by ~70% vs plain Minimax

### Task 4: Recommendation System (`task4_recommendation/recommender.py`)
- **Methods:** 
  - User-based Collaborative Filtering (Pearson correlation)
  - Item-based Collaborative Filtering
  - Content-Based Filtering (cosine similarity on item features)
  - Hybrid (weighted combination)
- **Features:** Movie recommendation demo with synthetic data, evaluation metrics (Precision@K, Recall@K, RMSE)
- **Demo:** Generates sample users with preferences, shows recommendations from each method

---

## 📝 Submission Checklist (CodSoft)

- [x] **≥3 tasks completed** (3/5 done)
- [x] **GitHub repo named `CODSOFT_TASKSNO`** ✅ https://github.com/ashishkushwaha138/CODSOFT_TASKSNO
- [ ] **Video demo** — Record yourself running each task (see demo commands above)
- [ ] **LinkedIn post** — Upload video, add `#codsoft` hashtag, tag @CODSOFT, include repo link
- [ ] **Submit form** — Use the Google Form link emailed by CodSoft

---

## 🎬 Demo Video Script (Suggested)

1. **Intro (10s):** "Hi, this is my CodSoft AI Internship submission — 3 tasks completed"
2. **Task 1 Chatbot (30s):** Run `python chatbot.py --demo`, show greetings, time, jokes, help
3. **Task 2 Tic-Tac-Toe (45s):** Run `python tictactoe_ai.py --play`, play a game, show AI blocks wins
4. **Task 4 Recommender (45s):** Run `python recommender.py`, show hybrid recommendations for different users
5. **Close (10s):** "Repo at github.com/ashishkushwaha138/CODSOFT_TASKSNO — thanks for watching!"

---

## 🌐 Live Demo

**Streamlit Cloud:** https://codsofttasks.streamlit.app/

---

## 📄 License

Educational project — CodSoft AI Internship 2026

---

**Repository:** https://github.com/ashishkushwaha138/CODSOFT_TASKSNO  
**Internship Portal:** www.codsoft.in