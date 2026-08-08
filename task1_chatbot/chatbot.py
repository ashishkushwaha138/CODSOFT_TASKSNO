#!/usr/bin/env python3
"""
Task 1: Rule-Based Chatbot
A simple chatbot that responds to user inputs based on predefined rules.
Uses pattern matching and if-else statements for natural language processing basics.
"""

import re
import random
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class RuleBasedChatbot:
    """A rule-based chatbot with pattern matching and contextual responses."""
    
    def __init__(self):
        self.name = "CodBot"
        self.context = {}
        self.conversation_history = []
        
        # Define patterns and responses
        self.patterns = {
            # Greetings
            r'\b(hi|hello|hey|greetings|howdy)\b': {
                'responses': [
                    "Hello there! How can I help you today?",
                    "Hi! Nice to see you. What's on your mind?",
                    "Hey! How's it going?",
                    "Greetings! What can I do for you?"
                ],
                'context': 'greeting'
            },
            
            # Goodbyes
            r'\b(bye|goodbye|see you|farewell|exit|quit)\b': {
                'responses': [
                    "Goodbye! Have a great day!",
                    "See you later! Take care!",
                    "Bye! Come back anytime!",
                    "Farewell! It was nice chatting with you!"
                ],
                'context': 'goodbye'
            },
            
            # Thanks
            r'\b(thanks|thank you|thx|ty)\b': {
                'responses': [
                    "You're welcome!",
                    "Happy to help!",
                    "Anytime!",
                    "No problem at all!"
                ],
                'context': 'thanks'
            },
            
            # Name queries
            r'\b(what.*your name|who are you|your name)\b': {
                'responses': [
                    f"I'm {self.name}, your friendly rule-based chatbot!",
                    f"You can call me {self.name}. Nice to meet you!",
                    f"I go by {self.name}. How can I assist you?"
                ],
                'context': 'identity'
            },
            
            # Time/date queries
            r'\b(what time|current time|time now|date today|today.*date)\b': {
                'responses': [self._get_time_response],
                'context': 'datetime'
            },
            
            # Weather (mock)
            r'\b(weather|temperature|forecast)\b': {
                'responses': [
                    "I don't have real-time weather access, but I hope it's nice where you are!",
                    "Check a weather app for accurate forecasts. I'm just a simple bot!",
                    "Sunny with a chance of code! ☀️ (I can't actually check weather)"
                ],
                'context': 'weather'
            },
            
            # Help
            r'\b(help|what can you do|commands|features)\b': {
                'responses': [self._get_help_response],
                'context': 'help'
            },
            
            # Jokes
            r'\b(joke|funny|laugh|humor)\b': {
                'responses': [
                    "Why don't scientists trust atoms? Because they make up everything! 😄",
                    "Why did the programmer quit his job? Because he didn't get arrays! 🤖",
                    "What's a computer's favorite snack? Microchips! 🍪",
                    "Why do Java developers wear glasses? Because they don't C#! 👓",
                    "There are 10 types of people: those who understand binary and those who don't. 💻"
                ],
                'context': 'joke'
            },
            
            # How are you
            r'\b(how are you|how.*doing|how.*going)\b': {
                'responses': [
                    "I'm doing great! Thanks for asking. How about you?",
                    "All systems operational! 🤖 Ready to chat.",
                    "Fantastic! Always happy to help. What's up with you?"
                ],
                'context': 'wellbeing'
            },
            
            # Age
            r'\b(how old|your age|age)\b': {
                'responses': [
                    "I'm timeless! Born when the code was written. 🕰️",
                    "Age is just a number, and I'm running on version 1.0!",
                    "I don't age like humans do. I just get updated!"
                ],
                'context': 'age'
            },
            
            # Favorite things
            r'\b(favorite|favourite|like most|prefer)\b': {
                'responses': [
                    "As a bot, I love clean code and bug-free programs! ✨",
                    "My favorite thing? Helping humans solve problems! 💡",
                    "I'm partial to Python, but I don't discriminate against other languages! 🐍"
                ],
                'context': 'preferences'
            },
            
            # Learning/AI questions
            r'\b(learn|study|ai|artificial intelligence|machine learning|ml)\b': {
                'responses': [
                    "Learning is awesome! What topic interests you?",
                    "AI and ML are fascinating fields. Are you working on a project?",
                    "Keep learning! Every expert was once a beginner. 📚"
                ],
                'context': 'learning'
            },
            
            # Compliments
            r'\b(smart|clever|intelligent|good job|well done|awesome|great)\b': {
                'responses': [
                    "Thanks! You're pretty awesome yourself! 😊",
                    "That's kind of you to say! Made my circuits happy! ⚡",
                    "Appreciate it! Keep being amazing!"
                ],
                'context': 'compliment'
            }
        }
        
        # Default responses for unmatched input
        self.default_responses = [
            "Interesting! Tell me more about that.",
            "I'm not sure I understand. Could you rephrase?",
            "That's a new one for me! What do you mean?",
            "Hmm, I don't have a rule for that yet. Want to teach me?",
            "I'm still learning! Try asking about time, jokes, or just say hi!"
        ]
    
    def _get_time_response(self) -> str:
        """Generate current time/date response."""
        now = datetime.now()
        return f"Current time: {now.strftime('%I:%M %p')}, Date: {now.strftime('%B %d, %Y')}"
    
    def _get_help_response(self) -> str:
        """Generate help response."""
        return (
            f"I'm {self.name}, a rule-based chatbot! Here's what I can do:\n"
            "• Greetings & farewells\n"
            "• Tell time & date\n"
            "• Tell jokes\n"
            "• Answer basic questions about myself\n"
            "• Chat about learning/AI topics\n\n"
            "Try saying: 'Hello', 'What time is it?', 'Tell me a joke', 'Help'"
        )
    
    def match_pattern(self, user_input: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Match user input against patterns. Returns (matched_rule, matched_pattern)."""
        user_input_lower = user_input.lower().strip()
        
        for pattern, rule in self.patterns.items():
            if re.search(pattern, user_input_lower, re.IGNORECASE):
                return rule, pattern
        return None, None
    
    def get_response(self, user_input: str) -> str:
        """Get chatbot response for user input."""
        # Store in history
        self.conversation_history.append({
            'user': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Match pattern
        rule, pattern = self.match_pattern(user_input)
        
        if rule:
            responses = rule['responses']
            # Handle callable responses (like time)
            if callable(responses[0]):
                response = responses[0]()
            else:
                response = random.choice(responses)
            
            # Update context
            self.context['last_topic'] = rule.get('context', 'general')
        else:
            response = random.choice(self.default_responses)
            self.context['last_topic'] = 'unknown'
        
        # Store bot response
        self.conversation_history.append({
            'bot': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def chat(self):
        """Main chat loop."""
        print(f"{self.name}: Hello! I'm {self.name}, your rule-based chatbot.")
        print(f"{self.name}: Type 'help' to see what I can do, or 'bye' to exit.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                response = self.get_response(user_input)
                print(f"{self.name}: {response}\n")
                
                # Check for goodbye
                rule, _ = self.match_pattern(user_input)
                if rule and rule.get('context') == 'goodbye':
                    break
                    
            except KeyboardInterrupt:
                print(f"\n{self.name}: Goodbye! 👋")
                break
            except EOFError:
                break
        
        print(f"\nConversation ended. History: {len(self.conversation_history)//2} exchanges")


def demo():
    """Run a quick demo without interactive input."""
    bot = RuleBasedChatbot()
    
    test_inputs = [
        "Hello there!",
        "What's your name?",
        "What time is it?",
        "Tell me a joke",
        "How are you?",
        "Thanks!",
        "Bye!"
    ]
    
    print("=" * 50)
    print("RULE-BASED CHATBOT DEMO")
    print("=" * 50)
    
    for user_input in test_inputs:
        print(f"\nYou: {user_input}")
        response = bot.get_response(user_input)
        print(f"{bot.name}: {response}")
    
    print("\n" + "=" * 50)
    print("Demo complete!")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        bot = RuleBasedChatbot()
        bot.chat()