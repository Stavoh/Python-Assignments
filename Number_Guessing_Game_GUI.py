import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        self.number = self.number_generator()
        self.attempts = 0
        self.hint_count = 0

        self.create_widgets()

    def number_generator(self):
        return random.randint(1, 20)

    def new_game(self):
        self.number = self.number_generator()
        self.attempts = 0
        self.hint_count = 0
        self.feedback_label.config(text="New game started! Guess the number.")
        self.guess_entry.delete(0, tk.END)

    def provide_hint(self):
        if self.hint_count < 3:
            if self.hint_count == 0:
                hint = f"The number is larger than {self.number - random.randint(3, 6)}. (Costs 2 attempts)"
                self.attempts += 2
            elif self.hint_count == 1:
                hint = f"The number is smaller than {self.number + random.randint(3, 6)}. (Costs 1 attempt)"
                self.attempts += 1
            elif self.hint_count == 2:
                hint = f"The number is between {self.number - random.randint(1, 3)} and {self.number + random.randint(1, 3)}. (Costs 1 attempt)"
                self.attempts += 1

            self.hint_count += 1
        else:
            hint = "You have used all your hints."

        self.feedback_label.config(text=hint)

    def cheat(self):
        messagebox.showinfo("Cheat", f"The number is {self.number}. Starting a new game.")
        self.new_game()

    def check_guess(self, event=None):
        guess = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END)
        
        if not guess.isdigit():
            self.feedback_label.config(text="Please enter a number between 1 and 20.")
            return

        guess = int(guess)
        if guess < 1 or guess > 20:
            self.feedback_label.config(text="Please enter a number between 1 and 20.")
            return

        self.attempts += 1

        if guess < self.number:
            self.feedback_label.config(text="Too small. Try again.")
        elif guess > self.number:
            self.feedback_label.config(text="Too big. Try again.")
        else:
            messagebox.showinfo("Congratulations!", f"Exactly! You won in {self.attempts} attempts with {self.hint_count} hints.")
            self.new_game()

    def exit_game(self):
        self.root.quit()

    def create_widgets(self):
        instruction_text = (
            "INSTRUCTIONS\n"
            "Guess the secret number between 1 and 20.\n"
            "MENU:\n"
            "New Game - Start a new game\n"
            "Hint - Get a hint (Costs attempts)\n"
            "Cheat - Reveal the number and restart\n"
            "Exit - Quit the game\n"
        )

        self.instructions_label = tk.Label(self.root, text=instruction_text, justify=tk.LEFT)
        self.instructions_label.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="New game started! Guess the number.", fg="blue")
        self.feedback_label.pack(pady=5)

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", self.check_guess)

        self.guess_button = tk.Button(self.root, text="Submit Guess", command=self.check_guess)
        self.guess_button.pack(pady=5)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=5)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.provide_hint)
        self.hint_button.pack(pady=5)

        self.cheat_button = tk.Button(self.root, text="Cheat", command=self.cheat)
        self.cheat_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit_game)
        self.exit_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
