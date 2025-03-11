from flask import Flask, request, jsonify
from model import solve_math_problem
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem')
    solution = solve_math_problem(problem)
    return jsonify({'problem': problem, 'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)
