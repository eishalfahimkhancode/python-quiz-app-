import json
import random
import tkinter as tk
from tkinter import messagebox


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz App")
        self.root.geometry("600x400")

        with open("data.json", "r") as f:
            self.questions = json.load(f)

        random.shuffle(self.questions)

        self.q_index = 0
        self.score = 0

        self.question_label = tk.Label(
            root, text="", wraplength=500, font=("Arial", 14), justify="left"
        )
        self.question_label.pack(pady=30)

        self.selected_option = tk.StringVar()
        self.option_buttons = []

        for i in range(4):
            rb = tk.Radiobutton(
                root,
                text="",
                variable=self.selected_option,
                value="",
                font=("Arial", 12),
                anchor="w",
                justify="left",
            )
            rb.pack(fill="x", padx=60, pady=5)
            self.option_buttons.append(rb)

        self.submit_button = tk.Button(
            root, text="Submit", command=self.check_answer, font=("Arial", 12)
        )
        self.submit_button.pack(pady=20)

        self.score_label = tk.Label(root, text="", font=("Arial", 12))
        self.score_label.pack()

        self.load_question()

    def load_question(self):
        if self.q_index < len(self.questions):
            q = self.questions[self.q_index]
            self.question_label.config(
                text=f"Q{self.q_index + 1}. {q['question']}"
            )
            self.selected_option.set(None)
            for i, option in enumerate(q["options"]):
                self.option_buttons[i].config(text=option, value=option)
        else:
            self.show_result()

    def check_answer(self):
        if self.q_index < len(self.questions):
            q = self.questions[self.q_index]
            chosen = self.selected_option.get()

            if chosen == "None" or chosen == "":
                messagebox.showwarning("Warning", "Please select an option!")
                return

            if chosen == q["answer"]:
                self.score += 1

            self.q_index += 1
            self.load_question()

    def show_result(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        result_label = tk.Label(
            self.root,
            text=f"Quiz Completed!\nYour Score: {self.score}/{len(self.questions)}",
            font=("Arial", 16),
        )
        result_label.pack(pady=100)

        restart_button = tk.Button(
            self.root, text="Restart", command=self.restart_quiz, font=("Arial", 12)
        )
        restart_button.pack()

    def restart_quiz(self):
        self.root.destroy()
        root = tk.Tk()
        QuizApp(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
