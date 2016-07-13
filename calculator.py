from flask import Flask, render_template, request

from equations import Equations
from postfixexpression import *
from polynomialsolver import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        err_start, err_end, message, expression = evaluate_infix(request.form['expression'])
        if err_start is None:
            return render_template('index.html', solution=message, expression=expression)
        else:
            if err_start != -1:
                return render_template('index.html',
                                       explanation=message,
                                       before_mistake=expression[:err_start],
                                       mistake=expression[err_start:err_end + 1],
                                       after_mistake=expression[err_end + 1:])
            else:
                return render_template('index.html',
                                       explanation=message,
                                       before_mistake=expression,
                                       mistake="",
                                       after_mistake="")


def evaluate_infix(expression):
    """
    The highest level function for evaluation of expressions
    :param expression: string representing an infix expression
    :return: err_start, err_end, message, interpreted expression in case of any error,
    None, None, solution, interpreted_expression otherwise
    """
    pat_unallowed = re.compile(r'([^A-Za-z0-9+\-*/=.,\s()])')
    if len(pat_unallowed.findall(expression)) > 0:
        pos = next(pat_unallowed.finditer(expression)).start()
        return pos, pos, "Unallowed symbol detected: %s" % expression[pos], expression

    if "=" in expression:  # Solve an equation
        if expression.count("=") > 1:
            pos = expression.index("=") + expression[expression.index("=") + 1:].index("=") + 1
            return pos, pos, "More than one '=' symbols in expression can't be interpreted", expression

        result = Equations.solve(*expression.split("="))
        if len(result) == 4:
            return result
        else:
            try:
                varname = result[0]
                polynomial = result[1]
                interpreted_expression = result[2]
            except (TypeError, IndexError):
                return -1, -1, "Something has gone terribly wrong", expression
    else:
        postfix_expression = PostfixExpression(expression)
        interpreted_expression = postfix_expression.interpreted_expression
        if postfix_expression.error_msg is not None:
            pos = postfix_expression.error_place
            return pos[0], pos[1], postfix_expression.error_msg, interpreted_expression
        else:
            varname = ""
            polynomial = postfix_expression.result.polynomial

    solver = PolynomialSolver()
    try:
        # Take the first (and the only) solution
        result = solver.solve(polynomial)[0]
    except NotImplementedError as e:
        return -1, -1, e.args[0], expression
    if result[1] == 0:
        if '=' in expression:
            return -1, -1, "The expression doesn't have a variable " + \
                   "(or the coefficient before it is 0), but " + \
                   "has a '=' sign. It cannot be interpreted.", expression
        # Formatting the result
        num_result = result[0] if math.floor(result[0]) != result[0] else math.floor(result[0])
        return None, None, str(num_result), interpreted_expression
    else:
        if '=' not in expression:
            return -1, -1, "The expression has variables but doesn't have '=' sign." + \
                   "Should it be treated as equation?", expression
        # Formatting the result
        num_result = result[0] if math.floor(result[0]) != result[0] else math.floor(result[0])
        return None, None, varname + ' = ' + str(num_result), interpreted_expression

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port }

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)
