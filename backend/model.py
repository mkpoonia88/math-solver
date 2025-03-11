import sympy as sp

def solve_math_problem(problem):
    try:
        result = sp.sympify(problem)
        solution = sp.solve(result)
        return str(solution)
    except Exception as e:
        return f"Error: {str(e)}"
