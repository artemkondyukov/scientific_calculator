import re

from expressionchecker import *
from operand import *


class PostfixExpression:
    def __init__(self):
        self.operators = {"+": lambda x, y: x + y,
                          "-": lambda x, y: x - y,
                          "*": lambda x, y: x * y,
                          "/": lambda x, y: x / y,
                          "~": lambda x: Operand([0]) - x}  # Unary '-' operator
        self.operator_precedences = {"+": 0, "-": 0, "*": 1, "/": 1, "~": 2}

        self.functions = {"log": lambda x, y: y.log(x),
                          "ln": lambda x: x.log(Operand([math.e]))}

        self.interpreted_expression = ""
        self.token_places = []  # An array of tuples (start_pos, end_pos) of tokens.
        self.error_msg = ""    # Last error in case of incorrect expression
        self.error_place = (-1, -1)  # Index of incorrect token
        self.varname = ""

    def tokenize(self, expr):
        """
        :param expr: the expression to process
        :return: an array of tokens from the string given
        """
        result = expr
        match = re.finditer(r'([A-Za-z]+)\(', result)  # Add implicit multiplication
        for m in match:
            if m.group(0)[:-1] not in self.functions:  # if we found a variable
                result = result[:m.end() - 1] + "*" + result[m.end() - 1:]

        result = re.sub(r'((?<=\d)([A-Za-z(]))', r'*\1', result)  # Add implicit multiplication
        result = re.sub(r'(^|\()-([A-Za-z0-9])', r'\1~\2', result)  # Replace usual - with unary operator
        result = re.sub(r'([(),*/+=~-])', r' \1 ', result)  # Add spaces around operators
        result = re.sub(r'([A-Za-z]+)', r' \1 ', result)  # Add spaces around variables and functions
        result = re.sub(r'(\s{2,})', r' ', result)  # Remove excess spaces
        result = result.split()
        self.interpreted_expression = "".join(result)
        start_pos = 0
        for token in result:
            end_pos = start_pos + len(token) - 1
            self.token_places.append((start_pos, end_pos))
            start_pos = end_pos + 1
        return result

    def is_expression_correct(self, token_array):
        """
        Constructs PDA for checking whether arithmetic expression is valid
        :param token_array: the value obtained from tokenize function
        :return: True if the expression is correct
        """
        checker = ExpressionChecker(operators=self.operators,
                                    functions=self.functions)
        result, error_place = checker.consume_token_array(token_array)
        if result is not None:
            self.error_msg = result
            self.error_place = self.token_places[error_place]
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
                                self.operator_precedences[token] <= self.operator_precedences[stack[-1]]:
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
            result.append(stack.pop())

        return result

    def process_postfix_array(self, postfix_array):
        """
        Does all calculation within an expression
        :param postfix_array: an array of tokens in postfix form
        :return: an Operand
        """
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
                        raise ValueError("Error: several names for variable: %s and %s" % (self.varname, element))

            elif element in self.operators:
                argcount = self.operators[element].__code__.co_argcount
                operands = []
                for i in range(argcount):
                    operands.append(operand_stack.pop())

                try:
                    operand_stack.append(self.operators[element](*operands[::-1]))
                except NotImplementedError as e:
                    self.error_msg = e.args[0]
                    return
                except ZeroDivisionError:
                    self.error_msg = "Division by zero detected!"
                    return

            elif element in self.functions:
                argcount = self.functions[element].__code__.co_argcount
                operands = []
                for i in range(argcount):
                    operands.append(operand_stack.pop())

                try:
                    operand_stack.append(self.functions[element](*operands[::-1]))
                except Exception as e:
                    self.error_msg = e.args[0].capitalize()
                    return

        return operand_stack[0]

    def process_infix_string(self, infix_string):
        """
        Does all processing required (tokenize, rewrite in postfix form and evaluate postfix)
        :param infix_string:
        :return: an Operand representing the result of a calculation
        """
        tokenized = self.tokenize(infix_string)
        if not tokenized:
            raise ValueError("Expression contains nothing. ")
        if not self.is_expression_correct(tokenized):
            raise ValueError(self.error_msg)
        postfix_array = self.convert_to_postfix(tokenized)
        result = self.process_postfix_array(postfix_array)
        if result is None:
            raise ValueError(self.error_msg)
        return result
