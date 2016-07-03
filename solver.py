import re

from operand import *


class Solver:
    def __init__(self):
        self.operators = {"+": lambda x, y: x + y,
                          "-": lambda x, y: x - y,
                          "*": lambda x, y: x * y,
                          "/": lambda x, y: x / y}
        self.op_precedences = {"+": 0, "-": 0, "*": 1, "/": 1}

        self.functions = {"log": lambda x, y: x.log(y),
                          "ln": lambda x: x.log(Operand([math.e]))}

        self.varname = ""

    def tokenize(self, expr):
        """
        :param expr: the expression to process
        :return: an array of tokens from the string given
        """
        match = re.finditer(r'([A-Za-z]+)\(', expr)  # Add implicit multiplication
        for m in match:
            if m.group(0)[:-1] not in self.functions:  # if we found a variable
                expr = expr[:m.end() - 1] + "*" + expr[m.end() - 1:]

        expr = re.sub(r'((?<=\d)([A-Za-z(]))', r'*\1', expr)  # Add implicit multiplication
        expr = re.sub(r'([(),*/+=-])', r' \1 ', expr)  # Add spaces around operators
        expr = re.sub(r'([A-Za-z]+)', r' \1 ', expr)  # Add spaces around variables and functions
        expr = re.sub(r'(\s{2,})', r' ', expr)  # Remove excess spaces
        return expr.split()

    def convert_to_postfix(self, token_array):
        """
        An implementation of Shunting-yard algorithm for arithmetic expression parsing
        :param token_array
        :return: an array representing the expression in postfix notation
        """
        result = []
        stack = []
        argcount_stack = [0]
        for token in token_array:
            if token.isalpha() and token not in self.functions:
                argcount_stack[-1] = 1 if argcount_stack[-1] == 0 else argcount_stack[-1]
                result.append(token)

            elif '.' in token:
                if not token.replace('.', '').isnumeric():
                    print("Error: point placed out of a number")
                    return
                else:
                    argcount_stack[-1] = 1 if argcount_stack[-1] == 0 else argcount_stack[-1]
                    if token.count('.') > 1:
                        print("Error: wrong number format: " + token)
                        return
                    result.append(token)

            elif token.isnumeric():
                argcount_stack[-1] = 1 if argcount_stack[-1] == 0 else argcount_stack[-1]
                result.append(token)

            elif token in self.operators:
                while len(stack) > 0 and stack[-1] in self.operators and \
                                self.op_precedences[token] <= self.op_precedences[stack[-1]]:
                    result.append(stack.pop())
                stack.append(token)

            elif token in self.functions:
                argcount_stack[-1] = 1 if argcount_stack[-1] == 0 else argcount_stack[-1]
                stack.append(token)

            elif token == "(":
                argcount_stack.append(0)
                stack.append(token)

            elif token == ")":
                while len(stack) > 0 and stack[-1] != "(":
                    result.append(stack.pop())
                if len(stack) == 0:
                    print("Error: unbalanced parentheses")
                    return
                if argcount_stack[-1] == 0:
                    print("Error: no operands in parentheses")
                    return
                stack.pop()  # Get rid of left parenthesis
                if len(stack) > 0 and stack[-1] in self.functions:
                    if self.functions[stack[-1]].__code__.co_argcount != argcount_stack[-1]:
                        print("Error: invalid number of arguments for function %s" % stack[-1])
                        return
                    result.append(stack.pop())
                    argcount_stack.pop()

            elif token == ",":
                argcount_stack[-1] += 1
                while len(stack) > 0 and stack[-1] != "(":
                    result.append(stack.pop())
                if len(stack) == 0:
                    print("Error: argument separator is put out of a function")
                    return

        while len(stack) > 0:
            if stack[-1] in list("()"):
                print("Error: unbalanced parentheses")
                return
            result.append(stack.pop())

        return result

    def process_postfix(self, postfix_array):
        operand_stack = []

        for element in postfix_array:
            if element not in self.operators and element not in self.functions:
                try:
                    operand_stack.append(Operand([float(element)]))
                except ValueError:
                    if self.varname == "":
                        self.varname = element
                        operand_stack.append(Operand([0., 1.]))
                    elif self.varname == element:
                        operand_stack.append(Operand([0., 1.]))
                    else:
                        print("Several names for variable: ", self.varname, element)
                        return

            elif element in self.operators:
                try:
                    right_op = operand_stack.pop()
                except IndexError:
                    print("No operands for operator ", element)
                    return
                try:
                    left_op = operand_stack.pop()
                except IndexError:
                    if element == "-":
                        left_op = Operand([0])
                    else:
                        print("Attempt to use operator '%s' as unary" % element)
                        return

                try:
                    operand_stack.append(self.operators[element](left_op, right_op))
                except NotImplementedError as e:
                    print(e.args[0])
                    return
                except ZeroDivisionError:
                    print("Division by zero detected!")
                    return

            elif element in self.functions:
                argcount = self.functions[element].__code__.co_argcount
                operands = []
                for i in range(argcount):
                    try:
                        operands.append(operand_stack.pop())
                    except IndexError:
                        print("Not enough arguments for function %s" % element)
                        return

                try:
                    operand_stack.append(self.functions[element](*operands))
                except NotImplementedError as e:
                    print(e.args[0])
                    return

        if len(operand_stack) > 1:
            print("Error: there is no operator between %s and %s" %
                  (operand_stack[0].varstring(self.varname), operand_stack[1].varstring(self.varname)))
            return

        return operand_stack[0].polynomial

    def solve(self, expression):
        self.varname = ""
        if "=" in expression:  # Solve an equation in case of '=' in expr
            if expression.count("=") > 1:
                print("More than one '=' symbols in expression can't be interpreted")
                return
            else:
                left_part = expression.split("=")[0]
                right_part = expression.split("=")[1]
                polynomial_left = []
                polynomial_right = []
                for expr, polynomial, tag in \
                        zip([left_part, right_part], [polynomial_left, polynomial_right], ["left", "right"]):
                    tokenized = self.tokenize(expr)
                    if not tokenized:
                        print(tag + " part contains nothing")
                        return

                    postfix = self.convert_to_postfix(tokenized)
                    if postfix is None:
                        return
                    tmp_polynomial = self.process_postfix(postfix)
                    if tmp_polynomial is None:
                        return
                    else:
                        polynomial.extend(tmp_polynomial)

            polynomial = (Operand(polynomial_left) - Operand(polynomial_right)).polynomial
        else:
            tokenized = self.tokenize(expression)
            postfix = self.convert_to_postfix(tokenized)
            if postfix is None:
                return
            polynomial = self.process_postfix(postfix)
            if polynomial is None:
                return

        if len(polynomial) == 1:
            num_result = polynomial[0] if math.floor(polynomial[0]) != polynomial[0] else math.floor(polynomial[0])
            return str(num_result)
        elif len(polynomial) == 2:
            if '=' not in expression:
                print("The expression has variables but doesn't have '=' sign.")
                print("Should it be treated as equation?")
                return
            num_result = -polynomial[0] / polynomial[1]
            num_result = num_result if math.floor(num_result) != num_result else num_result
            return self.varname + ' = ' + str(num_result)
        else:
            print("Only linear equations are supported by now!")
            return
