from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 SUBJECT-WISE QUESTIONS
questions = {
    "dsa": [
        "What is binary search?",
        "Explain linked list"
    ],
    "os": [
        "What is a process?",
        "Explain deadlock"
    ],
    "dbms": [
        "What is normalization?",
        "Explain SQL joins"
    ]
}

# 🔥 KEYWORDS FOR EVALUATION
answers_keywords = {
    "dsa": [
        ["sorted", "divide", "binary"],
        ["node", "pointer"]
    ],
    "os": [
        ["program", "execution"],
        ["deadlock", "resource"]
    ],
    "dbms": [
        ["normal", "redundancy"],
        ["join", "table"]
    ]
}

current_index = 0
current_subject = ""
total_score = 0

# 🆕 TRACK COMPLETED SUBJECTS
attended_subjects = set()

@app.route("/")
def home():
    return "Interview Chatbot Backend Running 🚀"

# ✅ GET QUESTION
@app.route("/question", methods=["GET"])
def get_question():
    global current_index, current_subject, total_score

    subject = request.args.get("subject")

    # 👉 When user selects subject
    if subject:
        # 🚫 Prevent reattempt
        if subject in attended_subjects:
            return jsonify({
                "question": "❌ You already attended this subject. You cannot take it again."
            })

        current_subject = subject
        current_index = 0
        total_score = 0

    if current_subject == "":
        return jsonify({"question": "Please select a subject first"})

    subject_questions = questions[current_subject]

    if current_index < len(subject_questions):
        return jsonify({"question": subject_questions[current_index]})
    else:
        # ✅ Mark subject as completed
        attended_subjects.add(current_subject)

        return jsonify({
            "question": f"🎉 Interview completed for {current_subject.upper()}",
            "total_score": total_score
        })

# 🔥 EVALUATION FUNCTION
def evaluate_answer(answer):
    global current_index, current_subject

    keywords = answers_keywords[current_subject][current_index]
    score = 0

    answer = answer.lower()

    for word in keywords:
        if word in answer:
            score += 2

    # Feedback
    if score >= 4:
        feedback = "Good answer 👍"
    elif score >= 2:
        feedback = "Average answer ⚠️"
    else:
        feedback = "Poor answer ❌"

    return score, feedback

# ✅ EVALUATE API
@app.route("/evaluate", methods=["POST"])
def evaluate():
    global current_index, total_score

    data = request.json
    answer = data.get("answer")

    if current_subject == "":
        return jsonify({"feedback": "Select subject first"})

    if current_index >= len(questions[current_subject]):
        return jsonify({"feedback": "Interview already completed"})

    score, feedback = evaluate_answer(answer)

    total_score += score
    current_index += 1

    return jsonify({
        "feedback": f"{feedback} (Score: {score})",
        "total_score": total_score
    })

if __name__ == "__main__":
    print("🚀 Server running...")
    app.run(debug=True)