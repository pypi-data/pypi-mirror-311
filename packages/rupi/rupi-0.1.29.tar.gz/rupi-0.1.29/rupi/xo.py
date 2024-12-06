import tkinter as tk
from tkinter import messagebox

def xo():
    # Initialize the game window
    window = tk.Tk()
    window.title("XO Game")
    
    # Initialize variables
    current_player = "X"
    board = [" " for _ in range(9)]
    
    def check_winner():
        """Check if there's a winner or if the game is a tie."""
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)              # Diagonal
        ]
        for combo in combos:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
                return board[combo[0]]
        if " " not in board:
            return "Tie"
        return None

    def button_click(index, button):
        """Handle button click."""
        nonlocal current_player

        if board[index] == " ":
            # Mark the board and update button text
            board[index] = current_player
            button.config(text=current_player)

            # Check for winner
            winner = check_winner()
            if winner:
                if winner == "Tie":
                    messagebox.showinfo("Game Over", "It's a Tie!")
                else:
                    messagebox.showinfo("Game Over", f"Player {winner} Wins!")
                window.quit()  # Close the window
                return
            
            # Switch player
            current_player = "O" if current_player == "X" else "X"
        else:
            messagebox.showwarning("Invalid Move", "This spot is already taken!")

    # Create a 3x3 grid of buttons
    buttons = []
    for i in range(9):
        button = tk.Button(
            window, text=" ", font=("Helvetica", 20), height=2, width=5,
            command=lambda i=i: button_click(i, buttons[i])
        )
        button.grid(row=i // 3, column=i % 3)
        buttons.append(button)

    # Start the Tkinter main loop
    window.mainloop()
