from flask import Flask, request, jsonify
from flask_cors import CORS
from model import solve_math

app = Flask(__name__)
CORS(app)

history = []

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    question = data.get('question')
    solution = solve_math(question)
    
    # Store in history
    history.append({"question": question, "solution": solution})
    
    return jsonify({"solution": solution})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    history.clear()
    return jsonify({"status": "History cleared"})

if __name__ == '__main__':
    app.run(debug=True)
