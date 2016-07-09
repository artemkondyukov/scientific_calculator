from flask import Flask, render_template, request

from postfixexpression import *
from polynomialsolver import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        err_start, err_end, message = evaluate_infix(request.form['expression'])
        expression = request.form['expression']
        if err_start is None:
            return render_template('index.html', solution=message, expression=expression)
        else:
            return render_template('index.html',
                                   explanation=message,
                                   before_mistake=expression[:err_start],
                                   mistake=expression[err_start:err_end+1],
                                   after_mistake=expression[err_end+1:])


def evaluate_infix(expression=None):
    """
    The highest level function for evaluation of expressions
    :param expression: string representing an infix expression
    :return: err_start, err_end, message in case of any error, None, None, solution otherwise
    """
    postfix_expression = PostfixExpression()
    if "=" in expression:  # Solve an equation
        if expression.count("=") > 1:
            pos = expression[expression.index("=")+1:].index("=")
            return pos, pos, "More than one '=' symbols in expression can't be interpreted"
        else:
            left_part = expression.split("=")[0]
            right_part = expression.split("=")[1]
            try:
                left_side_operand = postfix_expression.process_infix_string(left_part)
                right_side_operand = postfix_expression.process_infix_string(right_part)
            except ValueError as e:
                place = postfix_expression.error_place
                return place[0], place[1], e.args[0]

        polynomial = (left_side_operand - right_side_operand).polynomial
    else:
        try:
            polynomial = postfix_expression.process_infix_string(expression).polynomial
        except ValueError as e:
            place = postfix_expression.error_place
            return place[0], place[1], e.args[0]

    solver = PolynomialSolver()
    try:
        # Take the first (and the only) solution
        result = solver.solve(polynomial)[0]
    except NotImplementedError as e:
        return -1, -1, e.args[0]
    if result[1] == 0:
        if '=' in expression:
            return -1, -1, "The expression doesn't have a variable " + \
                           "(or the coefficient before it is 0), but " + \
                           "has a '=' sign. It cannot be interpreted."
        # Formatting the result
        num_result = result[0] if math.floor(result[0]) != result[0] else math.floor(result[0])
        return None, None, str(num_result)
    else:
        if '=' not in expression:
            return -1, -1, "The expression has variables but doesn't have '=' sign." + \
                           "Should it be treated as equation?"
        # Formatting the result
        num_result = result[0] if math.floor(result[0]) != result[0] else result[0]
        return None, None, postfix_expression.varname + ' = ' + str(num_result)
