import tkinter as tk
from tkinter import messagebox
import chess
import time


class ChessGame:
    def __init__(self, window, tile_size=75, colors=None):
        self.window = window
        self.tile_size = tile_size
        self.board = chess.Board()
        self.selected_square = None

        # Default colors if not provided
        self.colors = colors or {
            "black_tile": "#f0d9b5",
            "white_tile": "#b58863",
            "selected": "#3f9d9d",
            "legal_move": "#50C878",
            "invalid_move": "#ff0000",
            "text_black": "black",
            "text_white": "white",
        }

        self.pieces = {
            "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
            "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
        }

        # Set up the UI
        self._setup_ui()

    def _setup_ui(self):
        # Create canvas for chessboard
        self.chessboard_canvas = tk.Canvas(
            self.window,
            width=self.tile_size * 8,
            height=self.tile_size * 8
        )
        self.chessboard_canvas.pack()

        # Create canvas for turn indicator
        self.turn_indicator_canvas = tk.Canvas(
            self.window, width=self.tile_size * 8, height=self.tile_size
        )
        self.turn_indicator_canvas.pack()

        # Bind clicks to the chessboard
        self.chessboard_canvas.bind("<Button-1>", self.on_click)

        # Draw the board and turn indicator
        self.draw_board()
        self.draw_turn_indicator()

    def draw_board(self):
        self.chessboard_canvas.delete("all")
        for row in range(8):
            for col in range(8):
                color = (
                    self.colors["white_tile"]
                    if (row + col) % 2 == 0
                    else self.colors["black_tile"]
                )
                self.chessboard_canvas.create_rectangle(
                    col * self.tile_size,
                    row * self.tile_size,
                    (col + 1) * self.tile_size,
                    (row + 1) * self.tile_size,
                    fill=color,
                    outline="black",
                )
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_char = self.pieces.get(str(piece), None)
                    if piece_char:
                        text_color = (
                            self.colors["text_black"]
                            if piece.color == chess.WHITE
                            else self.colors["text_white"]
                        )
                        self.chessboard_canvas.create_text(
                            col * self.tile_size + self.tile_size // 2,
                            row * self.tile_size + self.tile_size // 2,
                            text=piece_char,
                            font=("Arial", self.tile_size // 2),
                            fill=text_color,
                        )

    def draw_turn_indicator(self):
        self.turn_indicator_canvas.delete("all")
        turn_text = "Black's Turn" if self.board.turn == chess.WHITE else "White's Turn"
        self.turn_indicator_canvas.create_text(
            self.tile_size * 4,
            self.tile_size // 2,
            text=turn_text,
            font=("Arial", 20),
            fill="black",
        )

    def mouse_to_square(self, event):
        col = event.x // self.tile_size
        row = 7 - (event.y // self.tile_size)
        return chess.square(col, row)

    def highlight_legal_moves(self, square):
        for move in self.board.legal_moves:
            if move.from_square == square:
                to_square = move.to_square
                col, row = chess.square_file(to_square), 7 - chess.square_rank(to_square)
                self.chessboard_canvas.create_rectangle(
                    col * self.tile_size,
                    row * self.tile_size,
                    (col + 1) * self.tile_size,
                    (row + 1) * self.tile_size,
                    outline=self.colors["legal_move"],
                    width=3,
                )

    def indicate_invalid_move(self, square):
        col, row = chess.square_file(square), 7 - chess.square_rank(square)
        rect = self.chessboard_canvas.create_rectangle(
            col * self.tile_size,
            row * self.tile_size,
            (col + 1) * self.tile_size,
            (row + 1) * self.tile_size,
            outline=self.colors["invalid_move"],
            width=4,
        )
        self.window.update()
        time.sleep(0.2)
        self.chessboard_canvas.delete(rect)

    def on_click(self, event):
        clicked_square = self.mouse_to_square(event)

        if self.selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece and piece.color == self.board.turn:
                self.selected_square = clicked_square
                self.highlight_legal_moves(self.selected_square)
            else:
                self.indicate_invalid_move(clicked_square)
        else:
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.draw_board()
                self.draw_turn_indicator()
                self.check_game_over()
            else:
                self.indicate_invalid_move(clicked_square)
            self.selected_square = None

    def check_game_over(self):
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Draw due to insufficient material.")
        elif self.board.is_seventyfive_moves():
            messagebox.showinfo("Game Over", "Draw due to the 75-move rule.")
        elif self.board.is_fivefold_repetition():
            messagebox.showinfo("Game Over", "Draw due to fivefold repetition.")
        else:
            return
        self.chessboard_canvas.unbind("<Button-1>")  # Disable further interaction


def play_chess():
    root = tk.Tk()
    root.title("Chess Game")
    ChessGame(root)
    root.mainloop()
