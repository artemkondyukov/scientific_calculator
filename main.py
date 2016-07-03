import re

from operand import *

VAR_NB = 1                      # By now calculator works with only one variable

operators = {"+": lambda x, y: x + y,
             "-": lambda x, y: x - y,
             "*": lambda x, y: x * y,
             "/": lambda x, y: x / y}
op_precedences = {"+": 0, "-": 0, "*": 1, "/": 1}

functions = {"log": lambda x, y: y.log(x),
             "ln": lambda x: x.log(Operand([math.e]))}


def tokenize(expr):
    """
    :param expr: the expression to process
    :return: an array of tokens from the string given
    """
    if "=" in expr:             # Solve an equation in case of '=' in expr
        if expr.count("=") > 1:
            print("Two '=' symbols in expression can't be interpreted")
            return
        idx = expr.index("=")
        processed = "(" + expr[:idx] + ")-(" + expr[idx+1:] + ")"
    else:
        processed = expr

    match = re.finditer(r'([A-Za-z]+)\(', processed)  # Add implicit multiplication
    for m in match:
        if m.group(0)[:-1] not in functions:          # if we found a variable
            processed = processed[:m.end()-1] + "*" + processed[m.end()-1:]

    processed = re.sub(r'((?<=\d)([A-Za-z(]))', r'*\1', processed)  # Add implicit multiplication
    processed = re.sub(r'([(),*/+=-])', r' \1 ', processed)  # Add spaces around operators
    processed = re.sub(r'([A-Za-z]+)', r' \1 ', processed)  # Add spaces around variables and functions
    processed = re.sub(r'(\s{2,})', r' ', processed)  # Remove excess spaces
    print(processed)
    return processed.split()


def convert_to_postfix(token_array):
    """
    An implementation of Shunting-yard algorithm for arithmetic expression parsing
    :param token_array
    :return: an array representing the expression in postfix notation
    """
    result = []
    stack = []
    for token in token_array:
        if token.isalpha() and token not in functions:
            result.append(token)

        elif token.replace('.', '').isnumeric():
            if token.count('.') > 1:
                print("Error: wrong number format: " + token)
            result.append(token)

        elif token in operators:
            while len(stack) > 0 and stack[-1] in operators and \
                            op_precedences[token] <= op_precedences[stack[-1]]:
                result.append(stack.pop())
            stack.append(token)

        elif token in functions or token == "(":
            stack.append(token)

        elif token == ")":
            while len(stack) > 0 and stack[-1] != "(":
                result.append(stack.pop())
            if len(stack) == 0:
                print("Error: unbalanced parentheses")
                return
            stack.pop()  # Get rid of left parenthesis
            if len(stack) > 0 and stack[-1] in functions:
                result.append(stack.pop())

        elif token == ",":
            while len(stack) > 0 and stack[-1] != "(":
                result.append(stack.pop())
            if len(stack) == 0:
                print("Error: unbalanced parentheses")
                return

    while len(stack) > 0:
        if stack[-1] in list("()"):
            print("Error: unbalanced parentheses")
        result.append(stack.pop())

    return result


def process_postfix(postfix_array):
    print(postfix_array)
    operand_stack = []

    varname = ""
    for element in postfix_array:
        if element not in operators and element not in functions:
            try:
                operand_stack.append(Operand([float(element)]))
            except ValueError:
                if varname == "":
                    varname = element
                    operand_stack.append(Operand([0., 1.]))
                elif varname == element:
                    operand_stack.append(Operand([0., 1.]))
                else:
                    print("Several names for variable: ", varname, element)
                    return

        elif element in operators:
            right_op = operand_stack.pop()
            try:
                left_op = operand_stack.pop()
            except IndexError:
                if element == "-":
                    left_op = Operand([0])
                else:
                    print("Attempt to use operator '%s' as unary" % element)
                    return

            operand_stack.append(operators[element](left_op, right_op))

        elif element in functions:
            argcount = functions[element].__code__.co_argcount
            operands = []
            for i in range(argcount):
                operands.append(operand_stack.pop())
            operand_stack.append(functions[element](*operands))

    print(operand_stack[0].polynomial)


expression = input()
# print(convert_to_postfix(tokenize(expression)))
print(process_postfix(convert_to_postfix(tokenize(expression))))
# while expression != "":
#     expression = input()
#     print(process_postfix(convert_to_postfix(tokenize(expression))))
