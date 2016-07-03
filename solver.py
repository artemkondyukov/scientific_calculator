import re

from operand import *


class Solver:
    def __init__(self):
        self.operators = {"+": lambda x, y: x + y,
                          "-": lambda x, y: x - y,
                          "*": lambda x, y: x * y,
                          "/": lambda x, y: x / y}
        self.op_precedences = {"+": 0, "-": 0, "*": 1, "/": 1}

        self.functions = {"log": lambda x, y: y.log(x),
                          "ln": lambda x: x.log(Operand([math.e]))}

    def tokenize(self, expr):
        """
        :param expr: the expression to process
        :return: an array of tokens from the string given
        """
        if "=" in expr:  # Solve an equation in case of '=' in expr
            if expr.count("=") > 1:
                print("Two '=' symbols in expression can't be interpreted")
                return
            idx = expr.index("=")
            processed = "(" + expr[:idx] + ")-(" + expr[idx + 1:] + ")"
        else:
            processed = expr

        match = re.finditer(r'([A-Za-z]+)\(', processed)  # Add implicit multiplication
        for m in match:
            if m.group(0)[:-1] not in self.functions:  # if we found a variable
                processed = processed[:m.end() - 1] + "*" + processed[m.end() - 1:]

        processed = re.sub(r'((?<=\d)([A-Za-z(]))', r'*\1', processed)  # Add implicit multiplication
        processed = re.sub(r'([(),*/+=-])', r' \1 ', processed)  # Add spaces around operators
        processed = re.sub(r'([A-Za-z]+)', r' \1 ', processed)  # Add spaces around variables and functions
        processed = re.sub(r'(\s{2,})', r' ', processed)  # Remove excess spaces
        print(processed)
        return processed.split()

    def convert_to_postfix(self, token_array):
        """
        An implementation of Shunting-yard algorithm for arithmetic expression parsing
        :param token_array
        :return: an array representing the expression in postfix notation
        """
        result = []
        stack = []
        for token in token_array:
            if token.isalpha() and token not in self.functions:
                result.append(token)

            elif token.replace('.', '').isnumeric():
                if token.count('.') > 1:
                    print("Error: wrong number format: " + token)
                result.append(token)

            elif token in self.operators:
                while len(stack) > 0 and stack[-1] in self.operators and \
                                self.op_precedences[token] <= self.op_precedences[stack[-1]]:
                    result.append(stack.pop())
                stack.append(token)

            elif token in self.functions or token == "(":
                stack.append(token)

            elif token == ")":
                argcount = 0
                while len(stack) > 0 and stack[-1] != "(":
                    argcount += 1
                    result.append(stack.pop())
                if len(stack) == 0:
                    print("Error: unbalanced parentheses")
                    return
                stack.pop()  # Get rid of left parenthesis
                if len(stack) > 0 and stack[-1] in self.functions:
                    if argcount != self.functions[stack[-1]].__code__.co_argcount:
                        print("Error: wrong number of arguments for function %s" % stack[-1])
                        return
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

    def process_postfix(self, postfix_array):
        print(postfix_array)
        operand_stack = []

        varname = ""
        for element in postfix_array:
            if element not in self.operators and element not in self.functions:
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

            elif element in self.operators:
                right_op = operand_stack.pop()
                try:
                    left_op = operand_stack.pop()
                except IndexError:
                    if element == "-":
                        left_op = Operand([0])
                    else:
                        print("Attempt to use operator '%s' as unary" % element)
                        return

                operand_stack.append(self.operators[element](left_op, right_op))

            elif element in self.functions:
                argcount = self.functions[element].__code__.co_argcount
                operands = []
                for i in range(argcount):
                    try:
                        operands.append(operand_stack.pop())
                    except IndexError:
                        print("Not enough arguments for function %s" % element)
                        return

                operand_stack.append(self.functions[element](*operands))

        return operand_stack[0].polynomial

    def solve(self, expression):
        tokenized = self.tokenize(expression)
        postfix = self.convert_to_postfix(tokenized)
        if postfix is None:
            return

        polynomial = self.process_postfix(postfix)
        if polynomial is None:
            return

        if len(polynomial) == 1:
            return polynomial[0]
        elif len(polynomial) == 2:
            return polynomial[0] / polynomial[1]
        else:
            raise NotImplementedError("Only linear equations are supported by now!")
