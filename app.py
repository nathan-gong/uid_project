from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-key"

DATA_FILE = os.path.join(os.path.dirname(__file__), "content.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

LESSON_COUNT = len(data["lessons"])
QUIZ_COUNT = len(data["quiz"])


def _init_session():
    session["activity"] = {
        "learn_entries": [],
        "quiz_answers": [],
        "started_at": datetime.utcnow().isoformat() + "Z",
    }


@app.route("/")
def index():
    _init_session()
    return render_template("index.html")


@app.route("/learn/<int:lesson_id>")
def learn(lesson_id):
    if lesson_id < 1 or lesson_id > LESSON_COUNT:
        return redirect(url_for("learn", lesson_id=1))

    lesson = next((item for item in data["lessons"] if item["id"] == lesson_id), None)
    if lesson is None:
        return redirect(url_for("learn", lesson_id=1))

    entry = {
        "lesson_id": lesson_id,
        "title": lesson["title"],
        "entered_at": datetime.utcnow().isoformat() + "Z",
    }
    session["activity"]["learn_entries"].append(entry)
    session.modified = True

    next_id = lesson_id + 1 if lesson_id < LESSON_COUNT else None
    prev_id = lesson_id - 1 if lesson_id > 1 else None
    return render_template(
        "learn.html",
        lesson=lesson,
        prev_id=prev_id,
        next_id=next_id,
        next_quiz_id=1 if lesson_id == LESSON_COUNT else None,
    )


@app.route("/quiz/<int:question_id>", methods=["GET", "POST"])
def quiz(question_id):
    if question_id < 1 or question_id > QUIZ_COUNT:
        return redirect(url_for("quiz", question_id=1))

    question = next((item for item in data["quiz"] if item["id"] == question_id), None)
    if question is None:
        return redirect(url_for("quiz", question_id=1))

    if request.method == "POST":
        selected = request.form.get("choice")
        entry = {
            "question_id": question_id,
            "selected": selected,
            "correct_answer": question["correct_answer"],
            "answered_at": datetime.utcnow().isoformat() + "Z",
        }
        session["activity"]["quiz_answers"].append(entry)
        session.modified = True

        if question_id < QUIZ_COUNT:
            return redirect(url_for("quiz", question_id=question_id + 1))
        return redirect(url_for("results"))

    session["activity"]["quiz_answers"].append({
        "question_id": question_id,
        "entered_at": datetime.utcnow().isoformat() + "Z",
    })
    session.modified = True

    prev_id = question_id - 1 if question_id > 1 else None
    return render_template(
        "quiz.html",
        question=question,
        prev_id=prev_id,
        next_id=question_id + 1 if question_id < QUIZ_COUNT else None,
    )


@app.route("/results")
def results():
    answers = [item for item in session["activity"]["quiz_answers"] if "selected" in item]
    score = sum(1 for answer in answers if answer["selected"] == answer["correct_answer"])
    total = len(answers)

    return render_template(
        "results.html",
        score=score,
        total=total,
        answers=answers,
        lessons=data["lessons"],
        quiz=data["quiz"],
    )


@app.route("/api/data")
def api_data():
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
