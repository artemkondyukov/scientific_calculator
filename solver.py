from postfixexpression import *
from polynomialsolver import *


class Solver:
    @staticmethod
    def evaluate_infix(expression):
        """
        The highest level function for evaluation of expressions
        :param expression: string representing an infix expression
        :return: None in case of any error, a fine-formatted string otherwise
        """
        postfix_expression = PostfixExpression()
        if "=" in expression:  # Solve an equation
            if expression.count("=") > 1:
                print("More than one '=' symbols in expression can't be interpreted")
                return
            else:
                left_part = expression.split("=")[0]
                right_part = expression.split("=")[1]
                try:
                    left_side_operand = postfix_expression.process_infix_string(left_part)
                    right_side_operand = postfix_expression.process_infix_string(right_part)
                except ValueError as e:
                    print(e.args[0])
                    return

            polynomial = (left_side_operand - right_side_operand).polynomial
        else:
            try:
                polynomial = postfix_expression.process_infix_string(expression).polynomial
            except ValueError as e:
                print(e.args[0])
                return

        solver = PolynomialSolver()
        result = solver.solve(polynomial)
        if result[1] == 0:
            if '=' in expression:
                print("The expression doesn't have a variable "
                      "(or the coefficient before it is 0), but "
                      "has a '=' sign. It cannot be interpreted.")
                return
            # Formatting the result
            num_result = result[0] if math.floor(result[0]) != result[0] else math.floor(result[0])
            return str(num_result)
        else:
            if '=' not in expression:
                print("The expression has variables but doesn't have '=' sign."
                      "Should it be treated as equation?")
                return
            num_result = result[0] if math.floor(result[0]) != result[0] else result[0]
            return postfix_expression.varname + ' = ' + str(num_result)
