from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🟢 Questions
questions = [
    "What is binary search?",
    "Explain OOP concepts",
    "What is a database?"
]

# 🟢 Keywords for evaluation
answers_keywords = [
    ["sorted", "divide", "log", "binary"],
    ["encapsulation", "inheritance", "polymorphism", "abstraction"],
    ["data", "storage", "database", "table"]
]

# 🟢 Global variables
current_index = 0
total_score = 0


# 🟢 Home route
@app.route("/")
def home():
    return "Interview Chatbot Backend Running 🚀"


# 🟢 Get Question (AUTO RESET FIXED)
@app.route("/question", methods=["GET"])
def get_question():
    global current_index, total_score

    # 🔥 Reset when interview completed
    if current_index >= len(questions):
        current_index = 0
        total_score = 0

    return jsonify({"question": questions[current_index]})


# 🟢 Evaluation Logic
def evaluate_answer(question_index, answer):
    keywords = answers_keywords[question_index]
    score = 0

    answer = answer.lower()

    for word in keywords:
        if word in answer:
            score += 2  # each keyword = 2 marks

    # 🟢 Feedback
    if score >= 8:
        feedback = "Excellent answer ✅"
    elif score >= 5:
        feedback = "Good answer 👍 but can improve"
    elif score >= 3:
        feedback = "Average answer ⚠️"
    else:
        feedback = "Poor answer ❌ try explaining more"

    return score, f"{feedback} (Score: {score}/10)"


# 🟢 Evaluate Route
@app.route("/evaluate", methods=["POST"])
def evaluate():
    global current_index, total_score

    data = request.json
    answer = data.get("answer", "")

    # If interview already completed
    if current_index >= len(questions):
        return jsonify({
            "feedback": "Interview already completed 🎉",
            "total_score": total_score
        })

    # Evaluate answer
    score, feedback = evaluate_answer(current_index, answer)

    total_score += score
    current_index += 1

    # 🔥 If last question → show final score
    if current_index >= len(questions):
        return jsonify({
            "feedback": feedback,
            "total_score": total_score,
            "message": "Interview completed 🎉"
        })

    return jsonify({
        "feedback": feedback,
        "total_score": total_score
    })


# 🟢 Run App (Docker-friendly)
if __name__ == "__main__":
    print("🚀 Server running...")
    app.run(host="0.0.0.0", port=5000)