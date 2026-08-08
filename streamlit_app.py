import streamlit as st
import sys
import os

# Add task directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'task1_chatbot'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'task2_tictactoe'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'task4_recommendation'))

# Page config
st.set_page_config(
    page_title="CODSOFT AI Internship Tasks",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .user-message {
        background: #667eea;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 2px;
    }
    .bot-message {
        background: #f1f3f4;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 2px;
    }
    .game-cell {
        width: 60px;
        height: 60px;
        border: 2px solid #667eea;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
    }
    .game-cell:hover {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 CODSOFT AI Internship Tasks</h1>
    <p>3 Completed Tasks • Rule-Based Chatbot • Tic-Tac-Toe AI • Recommendation System</p>
    <p><a href="https://github.com/ashishkushwaha138/CODSOFT_TASKSNO" target="_blank" style="color: #ffd700;">📁 GitHub Repository</a></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📋 Navigation")
task_choice = st.sidebar.radio(
    "Select Task",
    ["🏠 Overview", "💬 Task 1: Chatbot", "🎮 Task 2: Tic-Tac-Toe AI", "🎬 Task 4: Recommender"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### ℹ️ About
**CodSoft AI Virtual Internship**  
Completed 3/5 required tasks:
- ✅ Task 1: Rule-Based Chatbot
- ✅ Task 2: Tic-Tac-Toe AI (Minimax)
- ✅ Task 4: Recommendation System

[View on GitHub](https://github.com/ashishkushwaha138/CODSOFT_TASKSNO)
""")

# ============================================================
# TASK 1: CHATBOT
# ============================================================
if task_choice == "💬 Task 1: Chatbot":
    st.header("💬 Task 1: Rule-Based Chatbot")
    st.markdown("Pattern-matching chatbot with greetings, time, jokes, help, and more.")
    
    # Import chatbot
    from chatbot import RuleBasedChatbot
    
    # Initialize session state
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = RuleBasedChatbot()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Demo mode button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🎬 Run Demo", type="secondary"):
            demo_inputs = [
                "Hello there!",
                "What's your name?",
                "What time is it?",
                "Tell me a joke",
                "How are you?",
                "Thanks!",
                "Bye!"
            ]
            for user_input in demo_inputs:
                response = st.session_state.chatbot.get_response(user_input)
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("bot", response))
            st.rerun()
    
    # Chat display
    chat_container = st.container()
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-message user-message">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>CodBot:</strong> {message}</div>', unsafe_allow_html=True)
    
    # Input
    user_input = st.chat_input("Type your message...")
    if user_input:
        response = st.session_state.chatbot.get_response(user_input)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", response))
        st.rerun()
    
    # Clear button
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.chatbot = RuleBasedChatbot()
        st.rerun()

# ============================================================
# TASK 2: TIC-TAC-TOE
# ============================================================
elif task_choice == "🎮 Task 2: Tic-Tac-Toe AI":
    st.header("🎮 Task 2: Tic-Tac-Toe AI (Minimax + Alpha-Beta)")
    st.markdown("Unbeatable AI using Minimax algorithm with Alpha-Beta Pruning.")
    
    from tictactoe_ai import TicTacToe, MinimaxAI, Player, GameState
    
    # Initialize game state
    if "ttt_game" not in st.session_state:
        st.session_state.ttt_game = TicTacToe()
        st.session_state.ttt_ai = MinimaxAI(Player.O, True)
        st.session_state.ttt_human = Player.X
        st.session_state.ttt_ai_first = False
        st.session_state.ttt_game_over = False
    
    # Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 New Game", type="primary"):
            st.session_state.ttt_game = TicTacToe()
            st.session_state.ttt_ai = MinimaxAI(Player.O, True)
            st.session_state.ttt_human = Player.X
            st.session_state.ttt_game_over = False
            st.rerun()
    with col2:
        if st.button("🤖 AI First"):
            st.session_state.ttt_game = TicTacToe()
            st.session_state.ttt_ai = MinimaxAI(Player.X, True)
            st.session_state.ttt_human = Player.O
            st.session_state.ttt_game_over = False
            # AI makes first move
            move = st.session_state.ttt_ai.get_best_move(st.session_state.ttt_game)
            st.session_state.ttt_game.make_move(move, Player.X)
            st.rerun()
    with col3:
        st.metric("Nodes Evaluated", st.session_state.ttt_ai.nodes_evaluated if hasattr(st.session_state.ttt_ai, 'nodes_evaluated') else 0)
    
    # Game board
    game = st.session_state.ttt_game
    symbols = {Player.EMPTY: " ", Player.X: "❌", Player.O: "⭕"}
    colors = {Player.EMPTY: "#fff", Player.X: "#ff6b6b", Player.O: "#4ecdc4"}
    
    st.markdown("### Game Board")
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            cell = game.board[idx]
            with cols[j]:
                if cell == Player.EMPTY and game.game_state == GameState.ONGOING:
                    if st.button(" ", key=f"cell_{idx}", use_container_width=True):
                        if game.make_move(idx, st.session_state.ttt_human):
                            # Check game over
                            if not game.is_terminal():
                                # AI move
                                ai_move = st.session_state.ttt_ai.get_best_move(game)
                                game.make_move(ai_move, Player.O if st.session_state.ttt_human == Player.X else Player.X)
                            st.rerun()
                else:
                    st.markdown(
                        f'<div style="width: 80px; height: 80px; border: 2px solid #667eea; '
                        f'display: flex; align-items: center; justify-content: center; '
                        f'font-size: 32px; margin: 0 auto; background: {colors[cell]}; '
                        f'color: {"white" if cell != Player.EMPTY else "black"}; border-radius: 8px;">'
                        f'{symbols[cell]}</div>',
                        unsafe_allow_html=True
                    )
    
    # Game status
    st.markdown("---")
    if game.game_state == GameState.X_WINS:
        st.success("🎉 **X WINS!**" if st.session_state.ttt_human == Player.X else "🤖 **AI WINS!**")
    elif game.game_state == GameState.O_WINS:
        st.success("🎉 **O WINS!**" if st.session_state.ttt_human == Player.O else "🤖 **AI WINS!**")
    elif game.game_state == GameState.DRAW:
        st.info("🤝 **IT'S A DRAW!**")
    else:
        st.info(f"Your turn ({symbols[st.session_state.ttt_human]})")
    
    # Demo buttons
    st.markdown("### Demos")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎭 AI vs AI Demo"):
            # This would run in background - just show concept
            st.info("AI vs AI always draws with perfect play. Run locally with: `python tictactoe_ai.py --demo`")
    with col2:
        if st.button("📊 Benchmark"):
            st.info("Alpha-Beta reduces ~70% nodes vs plain Minimax. Run locally with: `python tictactoe_ai.py --benchmark`")

# ============================================================
# TASK 4: RECOMMENDER
# ============================================================
elif task_choice == "🎬 Task 4: Recommender":
    st.header("🎬 Task 4: Hybrid Recommendation System")
    st.markdown("Collaborative Filtering + Content-Based + Hybrid recommendations for movies.")
    
    from recommender import create_sample_data, HybridRecommender, FilterType
    import pandas as pd
    
    # Initialize recommender (cached)
    @st.cache_resource
    def load_recommender():
        ratings, movies = create_sample_data()
        recommender = HybridRecommender(cf_weight=0.6, cb_weight=0.4)
        recommender.fit(ratings, movies)
        return recommender, movies, ratings
    
    recommender, movies, ratings = load_recommender()
    
    # User selector
    user_ids = sorted(list(recommender.cf.user_item_matrix.keys()))
    selected_user = st.selectbox("Select User", user_ids, format_func=lambda x: f"User {x}")
    
    # Show user history
    if selected_user in recommender.cf.user_item_matrix:
        user_ratings = recommender.cf.user_item_matrix[selected_user]
        st.markdown(f"### 📜 {selected_user}'s Rating History ({len(user_ratings)} movies)")
        history_df = pd.DataFrame([
            {"Movie": movies[mid].name, "Genre": movies[mid].category, "Rating": f"{rating}/5"}
            for mid, rating in sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    # Recommendation method
    method = st.radio(
        "Recommendation Method",
        ["🤝 Hybrid (CF + CB)", "👥 Collaborative Filtering", "📊 Content-Based"],
        horizontal=True
    )
    
    method_map = {
        "🤝 Hybrid (CF + CB)": FilterType.HYBRID,
        "👥 Collaborative Filtering": FilterType.COLLABORATIVE,
        "📊 Content-Based": FilterType.CONTENT_BASED
    }
    
    # Get recommendations
    filter_type = method_map[method]
    recs = recommender.recommend(selected_user, 5, filter_type)
    
    st.markdown(f"### 🎯 Top 5 Recommendations ({method})")
    if recs:
        rec_df = pd.DataFrame([
            {"Rank": i+1, "Movie": movies[mid].name, "Genre": movies[mid].category, "Score": f"{score:.2f}/5"}
            for i, (mid, score) in enumerate(recs)
        ])
        st.dataframe(rec_df, use_container_width=True, hide_index=True)
        
        # Visualization
        st.bar_chart(pd.DataFrame({
            "Score": [score for _, score in recs]
        }, index=[movies[mid].name for mid, _ in recs]))
    else:
        st.warning("No recommendations available for this user with the selected method.")
    
    # Evaluation metrics
    with st.expander("📈 Model Evaluation (on training data)"):
        from recommender import evaluate_model
        metrics = evaluate_model(recommender, ratings, k=5)
        col1, col2, col3 = st.columns(3)
        col1.metric("Precision@5", f"{metrics['precision@k']:.3f}")
        col2.metric("Recall@5", f"{metrics['recall@k']:.3f}")
        col3.metric("RMSE", f"{metrics['rmse']:.3f}")

# ============================================================
# OVERVIEW
# ============================================================
else:
    st.header("📋 Project Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="task-card">
            <h3>💬 Task 1: Chatbot</h3>
            <p><strong>Type:</strong> Rule-Based NLP</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Pattern matching with regex</li>
                <li>Greetings, time, jokes, help</li>
                <li>Contextual responses</li>
                <li>Conversation history</li>
            </ul>
            <p><strong>Run locally:</strong></p>
            <code>python task1_chatbot/chatbot.py --demo</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="task-card">
            <h3>🎮 Task 2: Tic-Tac-Toe AI</h3>
            <p><strong>Algorithm:</strong> Minimax + Alpha-Beta</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Unbeatable AI opponent</li>
                <li>Human vs AI / AI vs AI</li>
                <li>Node evaluation benchmark</li>
                <li>~70% node reduction</li>
            </ul>
            <p><strong>Run locally:</strong></p>
            <code>python task2_tictactoe/tictactoe_ai.py --play</code>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="task-card">
            <h3>🎬 Task 4: Recommender</h3>
            <p><strong>Type:</strong> Hybrid (CF + CB)</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>User/Item Collaborative Filtering</li>
                <li>Content-Based (cosine similarity)</li>
                <li>Hybrid weighted combination</li>
                <li>Precision@K, Recall@K, RMSE</li>
            </ul>
            <p><strong>Run locally:</strong></p>
            <code>python task4_recommendation/recommender.py --demo</code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    ### 🚀 Deployment
    This Streamlit app is deployed on **Streamlit Cloud** (free).
    
    ### 📁 Repository
    **GitHub:** https://github.com/ashishkushwaha138/CODSOFT_TASKSNO
    
    ### 📝 Internship Submission
    - ✅ 3/5 tasks completed
    - ✅ GitHub repo: `CODSOFT_TASKSNO`
    - 🎬 Demo video needed for LinkedIn
    - 📋 Submit Google Form when received
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "CodSoft AI Internship 2026 • "
    "<a href='https://github.com/ashishkushwaha138/CODSOFT_TASKSNO' target='_blank'>GitHub</a> • "
    "<a href='https://www.codsoft.in' target='_blank'>CodSoft</a>"
    "</div>",
    unsafe_allow_html=True
)