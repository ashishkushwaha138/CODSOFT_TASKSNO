#!/usr/bin/env python3
"""
Task 2: Tic-Tac-Toe AI with Minimax Algorithm
An unbeatable AI agent that plays Tic-Tac-Toe against a human player.
Uses Minimax with Alpha-Beta Pruning for optimal play.
"""

import random
from typing import List, Tuple, Optional
from enum import Enum
from copy import deepcopy


class Player(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


class GameState(Enum):
    ONGOING = "ongoing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


class TicTacToe:
    """Tic-Tac-Toe game with Minimax AI."""
    
    WINNING_COMBINATIONS = [
        # Rows
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # Columns
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # Diagonals
        (0, 4, 8), (2, 4, 6)
    ]
    
    def __init__(self):
        self.board: List[Player] = [Player.EMPTY] * 9
        self.current_player = Player.X
        self.game_state = GameState.ONGOING
        self.winner: Optional[Player] = None
        self.move_history: List[Tuple[int, Player]] = []
    
    def reset(self):
        """Reset the game to initial state."""
        self.board = [Player.EMPTY] * 9
        self.current_player = Player.X
        self.game_state = GameState.ONGOING
        self.winner = None
        self.move_history = []
    
    def make_move(self, position: int, player: Player) -> bool:
        """Make a move at position (0-8). Returns True if valid."""
        if position < 0 or position > 8:
            return False
        if self.board[position] != Player.EMPTY:
            return False
        if self.game_state != GameState.ONGOING:
            return False
        
        self.board[position] = player
        self.move_history.append((position, player))
        self._check_game_state()
        return True
    
    def _check_game_state(self):
        """Check if game is over."""
        # Check wins
        for a, b, c in self.WINNING_COMBINATIONS:
            if (self.board[a] != Player.EMPTY and 
                self.board[a] == self.board[b] == self.board[c]):
                self.winner = self.board[a]
                self.game_state = (GameState.X_WINS if self.winner == Player.X 
                                   else GameState.O_WINS)
                return
        
        # Check draw
        if all(cell != Player.EMPTY for cell in self.board):
            self.game_state = GameState.DRAW
            return
        
        # Game ongoing
        self.game_state = GameState.ONGOING
    
    def get_available_moves(self) -> List[int]:
        """Return list of available positions."""
        return [i for i, cell in enumerate(self.board) if cell == Player.EMPTY]
    
    def is_terminal(self) -> bool:
        """Check if game is in terminal state."""
        return self.game_state != GameState.ONGOING
    
    def get_winner(self) -> Optional[Player]:
        """Return winner if any."""
        return self.winner
    
    def display_board(self):
        """Print the current board."""
        symbols = {Player.EMPTY: " ", Player.X: "X", Player.O: "O"}
        print("\n")
        for i in range(3):
            row = [symbols[self.board[i*3 + j]] for j in range(3)]
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i < 2:
                print("---+---+---")
        print("\n")
    
    def display_board_with_numbers(self):
        """Print board with position numbers for reference."""
        print("\nPosition guide:")
        for i in range(3):
            row = [str(i*3 + j + 1) for j in range(3)]
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if i < 2:
                print("---+---+---")
        print()


class MinimaxAI:
    """Minimax AI with Alpha-Beta Pruning for Tic-Tac-Toe."""
    
    def __init__(self, ai_player: Player = Player.O, use_alpha_beta: bool = True):
        self.ai_player = ai_player
        self.human_player = Player.X if ai_player == Player.O else Player.O
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
    
    def get_best_move(self, game: TicTacToe) -> int:
        """Get the best move using Minimax with Alpha-Beta Pruning."""
        self.nodes_evaluated = 0
        available = game.get_available_moves()
        
        if not available:
            return -1
        
        best_score = float('-inf')
        best_move = available[0]
        alpha = float('-inf')
        beta = float('inf')
        
        for move in available:
            # Make move
            game.make_move(move, self.ai_player)
            
            # Evaluate
            if self.use_alpha_beta:
                score = self._minimax(game, 0, False, alpha, beta)
            else:
                score = self._minimax(game, 0, False)
            
            # Undo move
            game.board[move] = Player.EMPTY
            game.game_state = GameState.ONGOING
            game.winner = None
            game.move_history.pop()
            
            if score > best_score:
                best_score = score
                best_move = move
            
            if self.use_alpha_beta:
                alpha = max(alpha, best_score)
        
        return best_move
    
    def _minimax(self, game: TicTacToe, depth: int, is_maximizing: bool, 
                 alpha: float = float('-inf'), beta: float = float('inf')) -> int:
        """Minimax algorithm with optional Alpha-Beta Pruning."""
        self.nodes_evaluated += 1
        
        # Terminal states
        if game.is_terminal():
            if game.get_winner() == self.ai_player:
                return 10 - depth  # Prefer faster wins
            elif game.get_winner() == self.human_player:
                return depth - 10  # Prefer slower losses
            else:
                return 0  # Draw
        
        available = game.get_available_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in available:
                game.make_move(move, self.ai_player)
                eval_score = self._minimax(game, depth + 1, False, alpha, beta)
                game.board[move] = Player.EMPTY
                game.game_state = GameState.ONGOING
                game.winner = None
                game.move_history.pop()
                
                max_eval = max(max_eval, eval_score)
                
                if self.use_alpha_beta:
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for move in available:
                game.make_move(move, self.human_player)
                eval_score = self._minimax(game, depth + 1, True, alpha, beta)
                game.board[move] = Player.EMPTY
                game.game_state = GameState.ONGOING
                game.winner = None
                game.move_history.pop()
                
                min_eval = min(min_eval, eval_score)
                
                if self.use_alpha_beta:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return min_eval


def play_game(ai_first: bool = False, use_alpha_beta: bool = True):
    """Play a game against the AI."""
    game = TicTacToe()
    ai_player = Player.X if ai_first else Player.O
    human_player = Player.O if ai_first else Player.X
    ai = MinimaxAI(ai_player, use_alpha_beta)
    
    print("=" * 50)
    print("TIC-TAC-TOE AI (Minimax + Alpha-Beta Pruning)")
    print("=" * 50)
    print(f"You are: {human_player.value}")
    print(f"AI is: {ai_player.value}")
    print(f"Alpha-Beta Pruning: {'Enabled' if use_alpha_beta else 'Disabled'}")
    game.display_board_with_numbers()
    
    if ai_first:
        print("AI goes first...")
        move = ai.get_best_move(game)
        game.make_move(move, ai_player)
        print(f"AI plays position {move + 1}")
        game.display_board()
    
    while game.game_state == GameState.ONGOING:
        # Human turn
        try:
            move_input = input(f"Your move (1-9): ").strip()
            if move_input.lower() in ['quit', 'exit', 'q']:
                print("Game quit.")
                return
            
            move = int(move_input) - 1
            if not game.make_move(move, human_player):
                print("Invalid move! Try again.")
                continue
        except ValueError:
            print("Please enter a number 1-9.")
            continue
        except KeyboardInterrupt:
            print("\nGame interrupted.")
            return
        
        game.display_board()
        
        if game.is_terminal():
            break
        
        # AI turn
        print("AI is thinking...")
        ai_move = ai.get_best_move(game)
        game.make_move(ai_move, ai_player)
        print(f"AI plays position {ai_move + 1} (nodes evaluated: {ai.nodes_evaluated})")
        game.display_board()
    
    # Game over
    print("=" * 50)
    if game.get_winner() == human_player:
        print("🎉 YOU WIN! Amazing!")
    elif game.get_winner() == ai_player:
        print("🤖 AI WINS! Better luck next time!")
    else:
        print("🤝 IT'S A DRAW! Well played!")
    print("=" * 50)


def demo_ai_vs_ai():
    """Demo: AI vs AI (should always draw with perfect play)."""
    print("\n" + "=" * 50)
    print("DEMO: AI vs AI (Perfect Play)")
    print("=" * 50)
    
    game = TicTacToe()
    ai_x = MinimaxAI(Player.X, True)
    ai_o = MinimaxAI(Player.O, True)
    
    turn = 0
    while game.game_state == GameState.ONGOING:
        current_ai = ai_x if turn % 2 == 0 else ai_o
        move = current_ai.get_best_move(game)
        player = Player.X if turn % 2 == 0 else Player.O
        game.make_move(move, player)
        print(f"Move {turn + 1}: {player.value} at position {move + 1} "
              f"(nodes: {current_ai.nodes_evaluated})")
        turn += 1
    
    game.display_board()
    if game.get_winner():
        print(f"Winner: {game.get_winner().value}")
    else:
        print("Result: DRAW (as expected with perfect play)")


def benchmark_alpha_beta():
    """Benchmark Alpha-Beta vs plain Minimax."""
    print("\n" + "=" * 50)
    print("BENCHMARK: Minimax vs Alpha-Beta Pruning")
    print("=" * 50)
    
    game = TicTacToe()
    
    # Test Alpha-Beta
    ai_ab = MinimaxAI(Player.O, True)
    move_ab = ai_ab.get_best_move(game)
    nodes_ab = ai_ab.nodes_evaluated
    
    # Test plain Minimax
    ai_plain = MinimaxAI(Player.O, False)
    move_plain = ai_plain.get_best_move(game)
    nodes_plain = ai_plain.nodes_evaluated
    
    print(f"Alpha-Beta Pruning: {nodes_ab} nodes evaluated")
    print(f"Plain Minimax:      {nodes_plain} nodes evaluated")
    print(f"Reduction:          {((nodes_plain - nodes_ab) / nodes_plain * 100):.1f}%")
    print(f"Best move (both):   {move_ab + 1}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            demo_ai_vs_ai()
        elif sys.argv[1] == '--benchmark':
            benchmark_alpha_beta()
        elif sys.argv[1] == '--play':
            ai_first = '--ai-first' in sys.argv
            use_ab = '--no-ab' not in sys.argv
            play_game(ai_first, use_ab)
    else:
        # Interactive play by default
        play_game()