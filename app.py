from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "hangman_secret_key"  # required for session

MAX_LIVES = 6


def load_word():
    with open("words.txt", "r") as f:
        words = f.read().splitlines()
    return random.choice(words).lower()


def init_game():
    session["word"] = load_word()
    session["guessed"] = []
    session["wrong"] = []
    session["lives"] = MAX_LIVES


@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        init_game()

    message = ""

    if request.method == "POST":
        guess = request.form.get("guess", "").lower()

        # Validation
        if not guess.isalpha() or len(guess) != 1:
            message = "Enter a single valid letter."
        elif guess in session["guessed"] or guess in session["wrong"]:
            message = "You already guessed that letter."
        elif guess in session["word"]:
            session["guessed"].append(guess)
        else:
            session["wrong"].append(guess)
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
        message=message
    )


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
