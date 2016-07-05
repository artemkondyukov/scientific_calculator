import re

from operand import *


class Solver:
    def __init__(self):
        self.operators = {"+": lambda x, y: x + y,
                          "-": lambda x, y: x - y,
                          "*": lambda x, y: x * y,
                          "/": lambda x, y: x / y,
                          "~": lambda x: Operand([0]) - x}  # Unary '-' operator
        self.op_precedences = {"+": 0, "-": 0, "*": 1, "/": 1, "~": 2}

        self.functions = {"log": lambda x, y: y.log(x),
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
        expr = re.sub(r'([(),*/+=~-])', r' \1 ', expr)  # Add spaces around operators
        expr = re.sub(r'([A-Za-z]+)', r' \1 ', expr)  # Add spaces around variables and functions
        expr = re.sub(r'(\s{2,})', r' ', expr)  # Remove excess spaces
        return expr.split()

    def check_correctness(self, token_array):
        """
        Constructs PDA for checking whether arithmetic expression is valid
        :param token_array: the value obtained from tokenize function
        :return: True if the expression is correct
        """
        PDA_states = {0: "operator", 1: "operand", 2: "parenthesis"}
        PDA_stack = []
        current_state = 1
        for i, token in enumerate(token_array):
            if token.count(".") > 1:
                print("Error: invalid number: %s" % token)
                return False
            if PDA_states[current_state] == "operand":
                if token in self.functions:
                    PDA_stack.append(token)
                    PDA_stack.append("(")
                    for _ in range(self.functions[token].__code__.co_argcount - 1):
                        PDA_stack.append("A")
                    current_state = 2
                elif token.replace(".", "").isalnum():
                    if token.isalpha():
                        if self.varname == "":
                                self.varname = token
                        else:
                            if token != self.varname:
                                print("Several names for variable: %s and %s" % (token, self.varname))
                                return False
                    current_state = 0
                elif token == "-":
                    if len(PDA_stack) > 0 and PDA_stack[-1] == "-":
                        print("Two unary '-' found for one operand")
                        return False
                    PDA_stack.append("-")
                    token_array[i] = '~'  # Replace usual '-' with unary -
                elif token == "(":
                    PDA_stack.append("(")
                else:  # token == "," or token == ")" or token in self.operators:
                    print("Expected operand but '%s' is given" % token)
                    return False

            elif PDA_states[current_state] == "operator":
                if token in self.operators:
                    current_state = 1
                elif token == ",":
                    if len(PDA_stack) == 0:
                        print("Error: ',' is put out of a function")
                        return False
                    elif PDA_stack[-1] == "(":
                        print("Error: unbalanced parentheses")
                        return False
                    elif PDA_stack[-1] == "A":
                        PDA_stack.pop()
                        current_state = 1
                elif token == ")":
                    if len(PDA_stack) == 0 or PDA_stack[-1] != "(":
                        print("Error: unbalanced parentheses")
                        return False
                    PDA_stack.pop()
                    if len(PDA_stack) > 0 and PDA_stack[-1] in self.functions:
                        PDA_stack.pop()
                else:  # token == "(" or token.replace(".", "").isalnum():
                    print("Error: expected operator, but '%s' is given" % token)
                    return False

            elif PDA_states[current_state] == "parenthesis":
                if token == "(":
                    current_state = 1
                else:
                    print("Error: '(' expected after function name, but '%s' is given" % token)
                    return False
        return True

    def convert_to_postfix(self, token_array):
        """
        An implementation of Shunting-yard algorithm for arithmetic expression parsing
        :param token_array
        :return: an array representing the expression in postfix notation
        """
        result = []
        stack = []
        for token in token_array:
            if token.replace(".", "").isalnum() and token not in self.functions:
                result.append(token)

            elif token in self.operators:
                while len(stack) > 0 and stack[-1] in self.operators and \
                                self.op_precedences[token] <= self.op_precedences[stack[-1]]:
                    result.append(stack.pop())
                stack.append(token)

            elif token in self.functions:
                stack.append(token)

            elif token == "(":
                stack.append(token)

            elif token == ")":
                while len(stack) > 0 and stack[-1] != "(":
                    result.append(stack.pop())
                stack.pop()  # Get rid of left parenthesis
                if len(stack) > 0 and stack[-1] in self.functions:
                    result.append(stack.pop())

            elif token == ",":
                while len(stack) > 0 and stack[-1] != "(":
                    result.append(stack.pop())

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
                print(operand_stack)
                argcount = self.operators[element].__code__.co_argcount
                operands = []
                for i in range(argcount):
                    try:
                        operands.append(operand_stack.pop())
                    except IndexError:
                        print("Not enough arguments for operator %s" % element)
                        return

                try:
                    operand_stack.append(self.operators[element](*operands[::-1]))
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
                    operand_stack.append(self.functions[element](*operands[::-1]))
                except NotImplementedError as e:
                    print(e.args[0])
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
                    if not self.check_correctness(tokenized):
                        return
                    postfix = self.convert_to_postfix(tokenized)
                    if postfix is None:
                        return
                    tmp_polynomial = self.process_postfix(postfix)
                    if tmp_polynomial is None:
                        return
                    else:
                        polynomial.extend(tmp_polynomial)

            print(polynomial_left, polynomial_right)
            polynomial = (Operand(polynomial_left) - Operand(polynomial_right)).polynomial
        else:
            tokenized = self.tokenize(expression)
            if not self.check_correctness(tokenized):
                return
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
