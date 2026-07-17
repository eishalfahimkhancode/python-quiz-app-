import json
import os
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

QUESTION_TIME = 15  # seconds per question
HIGH_SCORE_FILE = "highscores.json"


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz App")
        self.root.geometry("600x450")

        with open("data.json", "r") as f:
            self.questions = json.load(f)

        random.shuffle(self.questions)

        self.q_index = 0
        self.score = 0
        self.time_left = QUESTION_TIME
        self.timer_id = None

        # Ask for player name up front
        self.player_name = simpledialog.askstring(
            "Player Name", "Enter your name:", parent=self.root
        ) or "Player"

        # Timer label
        self.timer_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.timer_label.pack(pady=(15, 0))

        self.question_label = tk.Label(
            root, text="", wraplength=500, font=("Arial", 14), justify="left"
        )
        self.question_label.pack(pady=20)

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
            self.start_timer()
        else:
            self.show_result()

    def start_timer(self):
        self.time_left = QUESTION_TIME
        self.update_timer_label()
        self.run_timer()

    def run_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.timer_id = self.root.after(1000, self.run_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.q_index += 1
            self.load_question()

    def update_timer_label(self):
        self.timer_label.config(text=f"Time left: {self.time_left}s")

    def stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def check_answer(self):
        if self.q_index < len(self.questions):
            q = self.questions[self.q_index]
            chosen = self.selected_option.get()

            if chosen == "None" or chosen == "":
                messagebox.showwarning("Warning", "Please select an option!")
                return

            self.stop_timer()

            if chosen == q["answer"]:
                self.score += 1

            self.q_index += 1
            self.load_question()

    def show_result(self):
        self.stop_timer()

        for widget in self.root.winfo_children():
            widget.destroy()

        total = len(self.questions)
        self.save_high_score(self.player_name, self.score, total)
        top_scores = self.load_high_scores()

        result_label = tk.Label(
            self.root,
            text=f"Quiz Completed, {self.player_name}!\nYour Score: {self.score}/{total}",
            font=("Arial", 16),
        )
        result_label.pack(pady=30)

        board_label = tk.Label(
            self.root, text="Top Scores", font=("Arial", 14, "bold")
        )
        board_label.pack(pady=(10, 5))

        board_text = "\n".join(
            f"{i + 1}. {entry['name']} - {entry['score']}/{entry['total']}"
            for i, entry in enumerate(top_scores[:5])
        )
        scores_label = tk.Label(self.root, text=board_text, font=("Arial", 12))
        scores_label.pack(pady=5)

        restart_button = tk.Button(
            self.root, text="Restart", command=self.restart_quiz, font=("Arial", 12)
        )
        restart_button.pack(pady=20)

    def load_high_scores(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    scores = []
        else:
            scores = []
        scores.sort(key=lambda e: e["score"] / e["total"], reverse=True)
        return scores

    def save_high_score(self, name, score, total):
        scores = self.load_high_scores()
        scores.append({"name": name, "score": score, "total": total})
        scores.sort(key=lambda e: e["score"] / e["total"], reverse=True)
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f, indent=2)

    def restart_quiz(self):
        self.root.destroy()
        root = tk.Tk()
        QuizApp(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
