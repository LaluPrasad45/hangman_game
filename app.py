from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "hangman_secret_key"

DIFFICULTY_LIVES = {
    "easy": 8,
    "medium": 6,
    "hard": 4
}


def load_words():
    levels = {}
    with open("words.txt", "r") as f:
        for line in f:
            level, words = line.strip().split(":")
            levels[level] = words.split(",")
    return levels


WORDS = load_words()


def init_game(level="medium"):
    session["level"] = level
    session["word"] = random.choice(WORDS[level]).lower()
    session["guessed"] = []
    session["wrong"] = []
    session["lives"] = DIFFICULTY_LIVES[level]


@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        init_game()

    message = ""

    if request.method == "POST":
        if "level" in request.form:
            init_game(request.form["level"])
            return redirect(url_for("index"))

        guess = request.form.get("guess", "").lower()

        if not guess.isalpha() or len(guess) != 1:
            message = "Enter a single valid letter."
        elif guess in session["guessed"] or guess in session["wrong"]:
            message = "Already guessed."
        elif guess in session["word"]:
            guessed = session["guessed"]
            guessed.append(guess)
            session["guessed"] = guessed
        else:
            wrong = session["wrong"]
            wrong.append(guess)
            session["wrong"] = wrong
            session["lives"] -= 1


        

    word = session["word"]
    display_word = " ".join([c if c in session["guessed"] else "_" for c in word])

    win = all(c in session["guessed"] for c in word)
    lose = session["lives"] <= 0

    return render_template(
        "index.html",
        display_word=display_word,
        guessed=session["guessed"],
        wrong=session["wrong"],
        lives=session["lives"],
        win=win,
        lose=lose,
        word=word,
        message=message,
        level=session["level"]
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
