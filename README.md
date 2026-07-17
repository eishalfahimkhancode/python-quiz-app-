# Python Quiz App

A simple interactive quiz application built with **Tkinter** (GUI) and **JSON** (question storage). Test your knowledge with multiple-choice questions, a countdown timer, and a saved high-score leaderboard.

## Features

- Multiple-choice questions loaded from `data.json`
- Questions shuffle randomly each time you play
- 15-second countdown timer per question
- Score tracking with a results screen
- High-score leaderboard saved locally in `highscores.json`
- Restart button to play again instantly

## Requirements

- Python 3.7 or higher (Tkinter comes built-in with standard Python installs)

## How to Run

1. Clone this repository:
   ```
   git clone https://github.com/eishalfahimkhancode/python-quiz-app-.git
   cd python-quiz-app-
   ```

2. Run the app:
   ```
   python quiz.py
   ```

3. Enter your name, answer the questions before time runs out, and see your score and ranking at the end!

## Editing Questions

Questions are stored in `data.json` in this format:

```json
{
  "question": "What is the correct file extension for Python files?",
  "options": [".py", ".python", ".pt", ".pyt"],
  "answer": ".py"
}
```

Add, remove, or edit entries in this file to customize the quiz content.

## License

See [LICENSE](LICENSE) for details.
