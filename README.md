# CODSOFT_TASKSNO

**CodSoft AI Virtual Internship — Completed Tasks**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit_Cloud-FF4B4B.svg)](https://codsofttasks.streamlit.app/)

---

## 📋 Overview

This repository contains **3 completed tasks** for the **CodSoft Artificial Intelligence Virtual Internship**.  
**Requirement:** Complete at least 3 out of 5 tasks — ✅ **Done**

| Task | Title | Core Concept | Status |
|------|-------|--------------|--------|
| **1** | Rule-Based Chatbot | Regex pattern matching, NLP basics | ✅ Complete |
| **2** | Tic-Tac-Toe AI | Minimax + Alpha-Beta Pruning | ✅ Complete |
| **4** | Recommendation System | Collaborative + Content-Based + Hybrid | ✅ Complete |

> **Not implemented (optional):** Task 3 — Image Captioning, Task 5 — Face Detection & Recognition

---

## 🌐 Live Demo

**Streamlit Web App:** https://codsofttasks.streamlit.app/

Interactive browser version with all 3 tasks accessible via sidebar navigation.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Task 1 & 2: **No external dependencies** (stdlib only)
- Task 4: `numpy`, `pandas`

```bash
# Clone the repository
git clone https://github.com/ashishkushwaha138/CODSOFT_TASKSNO.git
cd CODSOFT_TASKSNO

# Install Task 4 dependencies
pip install numpy pandas
```

### Run Locally

<details>
<summary><strong>Task 1: Rule-Based Chatbot</strong></summary>

```bash
cd task1_chatbot

# Interactive chat
python chatbot.py

# Auto-demo (7 test cases)
python chatbot.py --demo
```
</details>

<details>
<summary><strong>Task 2: Tic-Tac-Toe AI</strong></summary>

```bash
cd task2_tictactoe

# Play against AI (you go first)
python tictactoe_ai.py --play

# AI goes first
python tictactoe_ai.py --play --ai-first

# AI vs AI perfect play demo
python tictactoe_ai.py --demo

# Benchmark: Alpha-Beta vs plain Minimax
python tictactoe_ai.py --benchmark
```
</details>

<details>
<summary><strong>Task 4: Recommendation System</strong></summary>

```bash
cd task4_recommendation

# Full demo with 10 users, 10 movies
python recommender.py --demo
```
</details>

---

## 📁 Project Structure

```
CODSOFT_TASKSNO/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── streamlit_app.py             # Web app (all 3 tasks)
├── task1_chatbot/
│   └── chatbot.py               # ~400 lines — Rule-based chatbot
├── task2_tictactoe/
│   └── tictactoe_ai.py          # ~450 lines — Minimax + Alpha-Beta
└── task4_recommendation/
    └── recommender.py           # ~600 lines — Hybrid recommender
```

---

## 🎯 Task Details

### Task 1: Rule-Based Chatbot
**`task1_chatbot/chatbot.py`**

- **13 intent categories** via regex pattern matching
- Greetings, goodbyes, thanks, identity, time/date, weather (mock), help, jokes, wellbeing, age, preferences, learning/AI, compliments
- Conversation history tracking, contextual responses, extensible rule system
- **Run:** `python chatbot.py --demo`

### Task 2: Tic-Tac-Toe AI
**`task2_tictactoe/tictactoe_ai.py`**

- **Minimax algorithm** with **Alpha-Beta Pruning**
- Unbeatable AI opponent (optimal play → always draw or win)
- Human vs AI, AI vs AI demo, node evaluation benchmark
- **~70% node reduction** vs plain Minimax
- **Run:** `python tictactoe_ai.py --play`

### Task 4: Hybrid Recommendation System
**`task4_recommendation/recommender.py`**

| Method | Technique |
|--------|-----------|
| Collaborative Filtering | User-based & Item-based (Pearson correlation) |
| Content-Based Filtering | Cosine similarity on item feature vectors |
| Hybrid | Weighted combination (default 0.6 CF + 0.4 CB) |

- **Demo data:** 10 movies × 10 users with genre preferences
- **Evaluation:** Precision@5, Recall@5, RMSE
- **Run:** `python recommender.py --demo`

---

## 🛠 Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.8+ |
| **Core Logic** | Standard library only (Tasks 1 & 2) |
| **Data/ML** | NumPy, Pandas, scikit-learn concepts (Task 4) |
| **Web App** | Streamlit |
| **Deployment** | Streamlit Cloud (free tier) |

---

## 📝 Submission Checklist

- [x] **≥3 tasks completed** (3/5)
- [x] **GitHub repo named `CODSOFT_TASKSNO`**
- [x] **Live demo deployed** (Streamlit Cloud)
- [ ] **Video demo** — Record terminal + web app
- [ ] **LinkedIn post** — Add `#codsoft`, tag `@CODSOFT`, include repo link
- [ ] **Submit Google Form** — Link emailed by CodSoft

---

## 🎬 Suggested Video Script (~3 min)

| Segment | Duration | Commands |
|---------|----------|----------|
| Intro | 10s | — |
| Task 1 Terminal | 30s | `python chatbot.py --demo` → interactive |
| Task 2 Terminal | 45s | `python tictactoe_ai.py --play` → play game → `--benchmark` |
| Task 4 Terminal | 45s | `python recommender.py --demo` |
| Streamlit Web App | 45s | Navigate all 3 tabs at live URL |
| Close | 10s | Show GitHub repo URL |

---

## 📄 License

Educational project — CodSoft AI Internship 2026

---

## 🔗 Links

| | |
|---|---|
| **GitHub Repository** | https://github.com/ashishkushwaha138/CODSOFT_TASKSNO |
| **Live Demo (Streamlit)** | https://codsofttasks.streamlit.app/ |
| **CodSoft Portal** | https://www.codsoft.in |

---

*Built for CodSoft AI Virtual Internship 2026*