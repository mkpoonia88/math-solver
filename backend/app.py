from flask import Flask, request, jsonify
from model import EnhancedCalculator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the solver
solver = EnhancedCalculator()

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem')

    if not problem:
        return jsonify({'error': 'No problem provided'}), 400

    try:
        if problem.lower().startswith('power('):
            params = problem[6:-1]
            result = solver.calculate_power(params)

        elif problem.lower().startswith('gcd('):
            numbers = problem[4:-1]
            result = solver.calculate_gcd(numbers)

        elif problem.lower().startswith('circle('):
            params = problem[7:-1]
            result = solver.calculate_circle(params)

        elif problem.lower().startswith('triangle('):
            params = problem[9:-1]
            result = solver.calculate_triangle(params)

        elif problem.lower().startswith('roots('):
            expr = problem[6:-1]
            result = solver.calculate_roots(expr)

        elif problem.lower().startswith('split('):
            expr = problem[6:-1]
            result = solver.split_middle_term(expr)

        elif 'and' in problem.lower():
            equations = problem.lower().split('and')
            result = solver.solve_system_of_equations([eq.strip() for eq in equations])

        elif '=' in problem:
            result = solver.solve_equation(problem)

        else:
            result = solver.evaluate_expression(problem)

        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
