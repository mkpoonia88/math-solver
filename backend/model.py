import re
import sympy as sp
from sympy import symbols, solve, sympify, gcd, sqrt, pi
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import math

class EnhancedCalculator:
    def _init_(self):
        self.x, self.y, self.z = symbols('x y z')
        self.transformations = standard_transformations + (implicit_multiplication_application,)

    def parse_equation(self, text):
        """Parse and clean the equation"""
        try:
            text = text.lower()
            text = re.sub(r'(\d+)([xyz])', r'\1 * \2', text)
            text = re.sub(r'([xyz])(\d+)', r'\1 * \2', text)
            
            equation_parts = re.split(r'\s*=\s*', text)
            if len(equation_parts) != 2:
                return f"Invalid equation: {text} (expected exactly one '=')"
            
            left_side = equation_parts[0].strip()
            right_side = equation_parts[1].strip()
            
            left_side = self.clean_expression(left_side)
            right_side = self.clean_expression(right_side)
            
            return f"{left_side} - ({right_side})"
        except Exception as e:
            return f"Error parsing equation: {str(e)}"

    def clean_expression(self, expr):
        """Clean the expression for SymPy parsing"""
        try:
            expr = expr.lower()
            expr = re.sub(r'plus|add', '+', expr)
            expr = re.sub(r'minus|subtract', '-', expr)
            expr = re.sub(r'times|multiply', '*', expr)
            expr = re.sub(r'divide by|divided by', '/', expr)
            expr = re.sub(r'squared', '**2', expr)
            expr = re.sub(r'cubed', '**3', expr)
            expr = re.sub(r'sqrt', 'sqrt', expr)
            expr = re.sub(r'power|pow', '', expr)
            expr = re.sub(r'\^', '', expr)
            expr = re.sub(r'(\d+)\s*power\s*(\d+)', r'\1**\2', expr)
            
            expr = re.sub(r'[^0-9xyz+\-/().pi sqrt*eE]', '', expr)
            expr = re.sub(r'\s+', ' ', expr)
            return expr.strip()
        except Exception as e:
            return f"Error cleaning expression: {str(e)}"

    def is_valid_expression(self, expr):
        """Validate if the expression is syntactically correct"""
        try:
            if not expr:
                return False, "Expression is empty"

            tokens = expr.split()
            for i in range(len(tokens) - 1):
                current_token = tokens[i]
                next_token = tokens[i + 1]
                
                is_current_number = bool(re.match(r'^-?\d*\.?\d+$', current_token))
                is_next_number = bool(re.match(r'^-?\d*\.?\d+$', next_token))
                
                if is_current_number and is_next_number:
                    suggestion = f"Did you mean '{current_token} * {next_token}' or '{current_token} + {next_token}'?"
                    return False, f"Missing operator between numbers '{current_token}' and '{next_token}'. {suggestion}"

            if re.search(r'[+\-/]{2,}', expr) and not re.search(r'\\*', expr):
                return False, "Invalid sequence of operators (e.g., '++', '*/')"

            return True, ""
        except Exception as e:
            return False, f"Error validating expression: {str(e)}"

    def evaluate_expression(self, expr):
        """Evaluate numerical expressions"""
        try:
            cleaned_expr = self.clean_expression(expr)
            valid, message = self.is_valid_expression(cleaned_expr)
            if not valid:
                return message
            
            result = parse_expr(cleaned_expr, 
                              local_dict={'pi': pi, 'sqrt': sqrt, 'pow': pow},
                              transformations=self.transformations).evalf()
            return result
        except Exception as e:
            return f"Unable to evaluate expression: {str(e)}"

    def calculate_power(self, params):
        """Calculate power (base^exponent)"""
        try:
            param_list = [float(p.strip()) for p in params.split(',')]
            if len(param_list) != 2:
                return "Please provide exactly two numbers: base,exponent"
            base, exponent = param_list
            return pow(base, exponent)
        except Exception as e:
            return f"Unable to calculate power: {str(e)}"

    def calculate_gcd(self, numbers):
        """Calculate GCD of given numbers"""
        try:
            nums = [int(float(n.strip())) for n in numbers.split(',')]
            if len(nums) < 2:
                return "Please provide at least two numbers for GCD calculation (separated by commas)"
            return gcd(*nums)
        except Exception as e:
            return f"Unable to calculate GCD: {str(e)}"

    def calculate_circle(self, params):
        """Calculate circle properties"""
        try:
            param_list = [float(p.strip()) for p in params.split(',')]
            
            if len(param_list) == 1:
                r = param_list[0]
                if r <= 0:
                    return "Radius must be positive"
                return {
                    'radius': r,
                    'diameter': 2 * r,
                    'circumference': 2 * pi * r,
                    'area': pi * r**2
                }
            elif len(param_list) == 2:
                x, y = param_list
                return {
                    'center': (x, y),
                    'equation': f"(x - {x})^2 + (y - {y})^2 = r^2 (radius not specified)"
                }
            else:
                return "Invalid parameters for circle calculation. Use: radius or x,y coordinates"
        except Exception as e:
            return f"Unable to calculate circle properties: {str(e)}"

    def calculate_triangle(self, params):
        """Calculate triangle properties"""
        try:
            param_list = [float(p.strip()) for p in params.split(',')]
            
            if len(param_list) == 3:
                a, b, c = param_list
                if any(side <= 0 for side in [a, b, c]):
                    return "Triangle sides must be positive"
                if (a + b <= c) or (b + c <= a) or (a + c <= b):
                    return "Invalid triangle: sides violate triangle inequality theorem"
                
                s = (a + b + c) / 2
                area = sqrt(s * (s - a) * (s - b) * (s - c))
                return {
                    'sides': (a, b, c),
                    'perimeter': a + b + c,
                    'semi-perimeter': s,
                    'area': area
                }
            elif len(param_list) == 2:
                base, height = param_list
                if base <= 0 or height <= 0:
                    return "Base and height must be positive"
                return {
                    'base': base,
                    'height': height,
                    'area': 0.5 * base * height
                }
            else:
                return "Invalid parameters for triangle calculation. Use: a,b,c (sides) or base,height"
        except Exception as e:
            return f"Unable to calculate triangle properties: {str(e)}"

    def calculate_roots(self, expr):
        """Calculate roots of an expression"""
        try:
            cleaned_expr = self.clean_expression(expr)
            expr = parse_expr(cleaned_expr, 
                           local_dict={'pi': pi, 'sqrt': sqrt, 'pow': pow},
                           transformations=self.transformations)
            roots = solve(expr, self.x)
            return roots if roots else "No real roots found"
        except Exception as e:
            return f"Unable to calculate roots: {str(e)}"

    def solve_equation(self, equation):
        """Solve the equation"""
        try:
            parsed_equation = self.parse_equation(equation)
            if "Invalid" in parsed_equation or "Error" in parsed_equation:
                return parsed_equation
            
            expr = sympify(parsed_equation, evaluate=False)
            solution = solve(expr, self.x)
            if not solution:
                return "No solution found"
            return solution
        except Exception as e:
            return f"Unable to solve equation: {str(e)}\nPlease check the equation format (e.g., use '*' for multiplication, ensure valid syntax)."

    def solve_system_of_equations(self, equations):
        """Solve a system of equations"""
        try:
            parsed_equations = []
            for eq in equations:
                parsed_eq = self.parse_equation(eq)
                if "Invalid" in parsed_eq or "Error" in parsed_eq:
                    return parsed_eq
                parsed_equations.append(parsed_eq)
            
            parsed_eqs = [sympify(eq) for eq in parsed_equations]
            solution = solve(parsed_eqs, (self.x, self.y), dict=True)
            if not solution:
                return "No solution found"
            return solution
        except Exception as e:
            return f"Unable to solve system: {str(e)}\nPlease check the equation format (e.g., use '*' for multiplication, ensure valid syntax)."

    def split_middle_term(self, expr):
        """Split the middle term for quadratic factorization"""
        try:
            cleaned_expr = self.clean_expression(expr)
            expr = parse_expr(cleaned_expr, 
                           local_dict={'pi': pi, 'sqrt': sqrt, 'pow': pow},
                           transformations=self.transformations)
            
            # Expand the expression to get coefficients
            expanded = sp.expand(expr)
            if expanded.is_polynomial(self.x) and expanded.degree(self.x) == 2:
                # Get coefficients ax^2 + bx + c
                a = expanded.coeff(self.x, 2)
                b = expanded.coeff(self.x, 1)
                c = expanded.coeff(self.x, 0)
                
                # Find factors of a*c that add up to b
                ac = a * c
                factors = []
                # Find all factor pairs of ac
                for i in range(-abs(int(ac)), abs(int(ac)) + 1):
                    if i == 0:
                        continue
                    if ac % i == 0:
                        j = ac // i
                        factors.append((i, j))
                        factors.append((-i, -j))
                
                # Find the pair that adds up to b
                split_terms = None
                for p, q in factors:
                    if p + q == b:
                        split_terms = (p, q)
                        break
                
                if split_terms:
                    p, q = split_terms
                    # Form the factored expression
                    result = {
                        'original': f"{a}x^2 + {b}x + {c}",
                        'split_terms': f"{a}x^2 + {p}x + {q}x + {c}",
                        'factors': f"({a}x + {p})(x + {q//a})" if a != 1 else f"(x + {p})(x + {q})",
                        'middle_terms': f"{p}x and {q}x (sum = {b}x, product = {ac})"
                    }
                    return result
                else:
                    return "Could not find suitable factors for middle term splitting"
            else:
                return "Expression must be a quadratic polynomial in x (ax^2 + bx + c)"
        except Exception as e:
            return f"Unable to split middle term: {str(e)}"

def main():
    solver = EnhancedCalculator()
    print("Welcome to the Enhanced Calculator!")
    print("Enter your equation or calculation (or type 'exit' to quit)")
    print("Examples:")
    print("- Equations: x^2 - 4 = 0, 2x + 3 = 7")
    print("- Systems: x + y = 5 and x - y = 1")
    print("- Basic calculations: 2 + 3 * 4")
    print("- Power: power(2,3) or 2**3 or 2^3 or 2 power 3")
    print("- GCD: gcd(48, 18)")
    print("- Circle: circle(5) or circle(2,3)")
    print("- Triangle: triangle(3,4,5) or triangle(6,8) (base,height)")
    print("- Roots: roots(x^2 - 4)")
    print("- Middle term split: split(x^2 + 5x + 6)")
    print("\nNote: Use '*' for multiplication (e.g., 2 * x instead of 2x).")
    print("Use 'pi' for π, 'sqrt' for square root.")
    print("For exponentiation, you can use '^' or '' or 'power'.")
    print("Decimal numbers are supported (e.g., 2.5)")
    print("\n")

    while True:
        problem = input("Enter your equation or calculation: ").strip()
        if problem.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not problem:
            print("Please enter a valid equation or calculation.")
            continue

        print(f"\nInput: {problem}")
        
        try:
            if problem.lower().startswith('power('):
                params = problem[6:-1]
                result = solver.calculate_power(params)
                print(f"Power result: {result}")
            
            elif problem.lower().startswith('gcd('):
                numbers = problem[4:-1]
                result = solver.calculate_gcd(numbers)
                print(f"GCD: {result}")
            
            elif problem.lower().startswith('circle('):
                params = problem[7:-1]
                result = solver.calculate_circle(params)
                print("Circle properties:", result)
            
            elif problem.lower().startswith('triangle('):
                params = problem[9:-1]
                result = solver.calculate_triangle(params)
                print("Triangle properties:", result)
            
            elif problem.lower().startswith('roots('):
                expr = problem[6:-1]
                result = solver.calculate_roots(expr)
                print(f"Roots: {result}")
            
            elif problem.lower().startswith('split('):
                expr = problem[6:-1]
                result = solver.split_middle_term(expr)
                print("Middle term splitting result:")
                if isinstance(result, dict):
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    print(result)
            
            elif 'and' in problem.lower():
                equations = problem.lower().split('and')
                result = solver.solve_system_of_equations([eq.strip() for eq in equations])
                print(f"Solution: {result}")
            
            elif '=' in problem:
                result = solver.solve_equation(problem)
                print(f"Solution: x = {result}")
            
            else:
                result = solver.evaluate_expression(problem)
                print(f"Result: {result}")
        except Exception as e:
            print(f"Error processing input: {str(e)}")
        
        print("\n")

if _name_ == "_main_":
    main()