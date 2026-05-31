from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "emye"

# Datasetleri yükle
with open("group1.txt", "r", encoding="utf-8") as f:
    group1 = [line.strip() for line in f.readlines()]

with open("group2.txt", "r", encoding="utf-8") as f:
    group2 = [line.strip() for line in f.readlines()]
    
@app.route("/")
def index():
    if "score" not in session:
        session["score"] = 0

    # Rastgele grup seç
    group_choice = random.choice([1, 2])

    if group_choice == 1:
        text = random.choice(group1)
    else:
        text = random.choice(group2)

    session["correct_group"] = group_choice
    session["current_text"] = text

    return render_template("index.html", text=text, score=session["score"])


@app.route("/guess", methods=["POST"])
def guess():
    user_guess = int(request.form["guess"])
    correct = session.get("correct_group")

    if user_guess == correct:
        session["score"] += 1
        return redirect("/")  # doğruysa yeni soru
    else:
        final_score = session["score"]
        session.clear()
        return render_template("gameover.html", score=final_score)  # ❌ yanlışsa bitir


if __name__ == "__main__":
    app.run(debug=True)