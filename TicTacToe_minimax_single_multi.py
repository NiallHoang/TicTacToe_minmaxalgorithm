from tkinter import *

# Main Application Class
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.geometry("330x550")
        self.root.title("Tic Tac Toe")
        self.root.resizable(0, 0)
        
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the main window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        titleLabel = Label(self.root, text="Tic Tac Toe", font=("Arial", 26), bg="orange", width=16)
        titleLabel.pack(pady=20)

        # Buttons
        singlePlayerButton = Button(self.root, text="Singleplayer", width=20, height=2, font=("Arial", 15), command=self.start_single_player)
        singlePlayerButton.pack(pady=10)

        multiPlayerButton = Button(self.root, text="Multiplayer", width=20, height=2, font=("Arial", 15), command=self.start_multi_player)
        multiPlayerButton.pack(pady=10)

        settingsButton = Button(self.root, text="Settings", width=20, height=2, font=("Arial", 15), command=self.open_settings)
        settingsButton.pack(pady=10)

    def start_single_player(self):
        self.mode = "singlePlayer"
        self.start_game()

    def start_multi_player(self):
        self.mode = "multiPlayer"
        self.start_game()

    def open_settings(self):
        # Placeholder for settings functionality
        settingsLabel = Label(self.root, text="Settings (Coming Soon)", font=("Arial", 20))
        settingsLabel.pack(pady=20)

    def start_game(self):
        # Clear the main window for the game
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame1 = Frame(self.root)
        self.frame1.pack()
        self.titleLabel = Label(self.frame1, text="Tic Tac Toe", font=("Arial", 26), bg="orange", width=16)
        self.titleLabel.grid(row=0, column=0)

        self.optionFrame = Frame(self.root, bg="grey")
        self.optionFrame.pack()

        self.frame2 = Frame(self.root, bg="yellow")
        self.frame2.pack()

        self.board = {1: " ", 2: " ", 3: " ",
                      4: " ", 5: " ", 6: " ",
                      7: " ", 8: " ", 9: " "}

        self.turn = "x"
        self.game_end = False

        self.create_game_buttons()
        
        # Restart Button
        self.restartButton = Button(self.frame2, text="Restart Game", width=19, height=1, font=("Arial", 20), bg="Green", command=self.restart_game)
        self.restartButton.grid(row=4, column=0, columnspan=3)

        # Return to Main Menu Button
        self.returnButton = Button(self.frame2, text="Return to Menu", width=19, height=1, font=("Arial", 20), bg="blue", command=self.create_main_menu)
        self.returnButton.grid(row=5, column=0, columnspan=3)

    def create_game_buttons(self):
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = Button(self.frame2, text=" ", width=4, height=2, font=("Arial", 30), bg="yellow", relief=RAISED, borderwidth=5)
                button.grid(row=i, column=j)
                button.bind("<Button-1>", self.play)
                self.buttons.append(button)

    def update_board(self):
        for key in self.board.keys():
            self.buttons[key-1]["text"] = self.board[key]

    def check_for_win(self, player):
        return ((self.board[1] == self.board[2] == self.board[3] == player) or
                (self.board[4] == self.board[5] == self.board[6] == player) or
                (self.board[7] == self.board[8] == self.board[9] == player) or
                (self.board[1] == self.board[4] == self.board[7] == player) or
                (self.board[2] == self.board[5] == self.board[8] == player) or
                (self.board[3] == self.board[6] == self.board[9] == player) or
                (self.board[1] == self.board[5] == self.board[9] == player) or
                (self.board[3] == self.board[5] == self.board[7] == player))

    def check_for_draw(self):
        return all(self.board[i] != " " for i in self.board)

    def play(self, event):
        if self.game_end:
            return

        button = event.widget
        clicked = self.buttons.index(button) + 1  # Get the button index to map to the board

        if button["text"] == " ":
            self.board[clicked] = self.turn
            self.update_board()

            if self.check_for_win(self.turn):
                winningLabel = Label(self.frame1, text=f"{self.turn} wins the game", bg="orange", font=("Arial", 26), width=16)
                winningLabel.grid(row=0, column=0, columnspan=3)
                self.game_end = True
                return

            if self.check_for_draw():
                drawLabel = Label(self.frame1, text="Game Draw", bg="orange", font=("Arial", 26), width=16)
                drawLabel.grid(row=0, column=0, columnspan=3)
                self.game_end = True
                return

            # Switch turns
            self.turn = "o" if self.turn == "x" else "x"

            # Handle single-player mode
            if self.mode == "singlePlayer" and self.turn == "o":
                self.play_computer()
                self.update_board()
                if self.check_for_win(self.turn):
                    winningLabel = Label(self.frame1, text=f"{self.turn} wins the game", bg="orange", font=("Arial", 26), width=16)
                    winningLabel.grid(row=0, column=0, columnspan=3)
                    self.game_end = True
                if self.check_for_draw() and not self.game_end:
                    drawLabel = Label(self.frame1, text="Game Draw", bg="orange", font=("Arial", 26), width=16)
                    drawLabel.grid(row=0, column=0, columnspan=3)
                    self.game_end = True
                self.turn = "x"  # Switch back to player

    def play_computer(self):
        bestScore = -100
        bestMove = 0
        for key in self.board.keys():
            if self.board[key] == " ":
                self.board[key] = "o"
                score = self.minimax(self.board, False)
                self.board[key] = " "
                if score > bestScore:
                    bestScore = score
                    bestMove = key
        self.board[bestMove] = "o"

    def minimax(self, board, isMaximizing):
        if self.check_for_win("o"):
            return 1
        if self.check_for_win("x"):
            return -1
        if self.check_for_draw():
            return 0

        if isMaximizing:
            bestScore = -100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "o"
                    score = self.minimax(board, False)
                    board[key] = " "
                    bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 100
            for key in board.keys():
                if board[key] == " ":
                    board[key] = "x"
                    score = self.minimax(board, True)
                    board[key] = " "
                    bestScore = min(score, bestScore)
            return bestScore

    def restart_game(self):
        self.game_end = False
        self.turn = "x"  # Reset to player 'x'
        for button in self.buttons:
            button["text"] = " "
        for i in self.board.keys():
            self.board[i] = " "
        self.update_board()
        self.titleLabel.config(text="Tic Tac Toe")  # Reset title

# Create the main window
if __name__ == "__main__":
    root = Tk()
    game = TicTacToe(root)
    root.mainloop()
