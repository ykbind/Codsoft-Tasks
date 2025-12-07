import tkinter as tk
from tkinter import ttk
import random


class RPSGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rock-Paper-Scissors Game")
        self.geometry("450x350")
        self.resizable(False, False)

        self.choices = ["Rock", "Paper", "Scissors"]

        # Score
        self.user_score = 0
        self.comp_score = 0

        self.user_choice_var = tk.StringVar()
        self.comp_choice_var = tk.StringVar()
        self.result_var = tk.StringVar()
        self.score_var = tk.StringVar(value="User: 0 | Computer: 0")

        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Rock - Paper - Scissors", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        instruction = ttk.Label(self, text="Choose your move:")
        instruction.pack()

        # Buttons for choices
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Rock", command=lambda: self.play_round("Rock")).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Paper", command=lambda: self.play_round("Paper")).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text="Scissors", command=lambda: self.play_round("Scissors")).grid(row=0, column=2, padx=10)

        # Display user & computer choices
        choice_frame = ttk.Frame(self)
        choice_frame.pack(pady=10)

        ttk.Label(choice_frame, text="Your Choice:").grid(row=0, column=0, sticky="w")
        ttk.Label(choice_frame, textvariable=self.user_choice_var, foreground="blue").grid(row=0, column=1, sticky="w")

        ttk.Label(choice_frame, text="Computer's Choice:").grid(row=1, column=0, sticky="w")
        ttk.Label(choice_frame, textvariable=self.comp_choice_var, foreground="red").grid(row=1, column=1, sticky="w")

        # Result display
        ttk.Label(self, textvariable=self.result_var, font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Score display
        ttk.Label(self, textvariable=self.score_var, font=("Segoe UI", 12)).pack(pady=10)

        # Play again button
        ttk.Button(self, text="Play Again", command=self.reset_round).pack(pady=5)

    def play_round(self, user_choice):
        comp_choice = random.choice(self.choices)

        self.user_choice_var.set(user_choice)
        self.comp_choice_var.set(comp_choice)

        result = self.determine_winner(user_choice, comp_choice)
        self.result_var.set(result)

        # Update score
        if result == "You Win!":
            self.user_score += 1
        elif result == "You Lose!":
            self.comp_score += 1

        self.score_var.set(f"User: {self.user_score} | Computer: {self.comp_score}")

    def determine_winner(self, user, comp):
        if user == comp:
            return "It's a Tie!"

        if (
            (user == "Rock" and comp == "Scissors") or
            (user == "Paper" and comp == "Rock") or
            (user == "Scissors" and comp == "Paper")
        ):
            return "You Win!"

        return "You Lose!"

    def reset_round(self):
        self.user_choice_var.set("")
        self.comp_choice_var.set("")
        self.result_var.set("")


if __name__ == "__main__":
    RPSGame().mainloop()
