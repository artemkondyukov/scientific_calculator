from itertools import compress, count, islice
from functools import partial
from operator import eq
from pda import PDA
import re


class ExpressionChecker(PDA):
    def __init__(self, operators, functions):
        """
        Creates an arithmetic expression checker based on push-down automaton
        It has three states: awaiting operand, awaiting operator and awaiting parenthesis (after function)
        By now supports expressions with only variable
        :param operators: a dictionary (operator_name: string, operator_function: function)
        :param functions: a dictionary (function_name: string, function_body: function)
        :return:
        """
        states = {"operator": self.__state_operator,
                  "operand": self.__state_operand,
                  "parenthesis": self.__state_parenthesis}
        super().__init__(states, current_state="operand")

        self.operators = operators
        self.functions = functions
        self.variable_name = ""

    def consume_token_array(self, token_array):
        """
        Checks whether a string given belongs to the language recognized by a PDA
        :param token_array:
        :return: (None, None) if a string does belong and tuple (error string, token number) otherwise
        if an error appears at the end of a token array, instead of token number -1 is returned
        """

        def nth_item(num, item, iterable):
            indices = compress(count(), map(partial(eq, item), iterable))
            return next(islice(indices, num, None), -1)

        self.current_state = "operand"
        self.stack = []
        self.variable_name = ""

        for i, token in enumerate(token_array):
            if len(re.findall(r"[^A-Za-z0-9+~\-*/.,()]", token)) != 0:
                raise ValueError("Unallowed character in token array: %s.", token)
            if token.count(".") > 1:
                return "Error: invalid number.", i
            result = self.consume_token(token)
            if result is not None:
                return result, i
        if self.current_state == "parenthesis":
            return "Error: '(' is expected after a function name, but the end of the expression reached.", -1
        if self.current_state == "operand":
            return "Error: operand is expected, but the end of the expression reached.", -1
        if len(self.stack) > 0:
            if self.stack[-1] == "(":
                n = token_array.count("(") - token_array.count(")") - 1
                print(n)
                pos = nth_item(n, "(", token_array)
                return "Error: unbalanced parentheses.", pos
            elif self.stack[-1] == "A":
                last_function_name, idx = "", -1
                for i in range(1, len(self.stack) + 1):
                    if self.stack[-i] in self.functions:
                        last_function_name = self.stack[-i]
                        idx = len(self.stack) - i - 1
                        break
                return "Error: wrong number of arguments for function %s." % last_function_name, idx
        return None, None

    def __state_operator(self, token):
        if token in self.operators:
            self.current_state = "operand"
        elif token == ",":
            if len(self.stack) == 0:
                return "Error: ',' is put out of a function."
            elif self.stack[-1] == "(":
                if len(self.stack) > 1:
                    if self.stack[-2] in self.functions:
                        return "Error: wrong number of arguments for function %s." % self.stack[-2]
                return "Error: ',' is put out of a function."
            elif self.stack[-1] == "A":
                self.stack.pop()
                self.current_state = "operand"
        elif token == ")":
            if len(self.stack) == 0:
                return "Error: unbalanced parentheses."
            if self.stack[-1] == "A":
                last_function = [token for token in self.stack[::-1] if token in self.functions][0]
                return "Error: wrong number of arguments for function %s." % last_function
            self.stack.pop()
            if len(self.stack) > 0 and self.stack[-1] in self.functions:
                self.stack.pop()
        else:
            return "Error: expected operator, but '%s' is given." % token

    def __state_operand(self, token):
        if token in self.functions:
            if len(self.stack) > 0 and self.stack[-1] == "~":
                self.stack.pop()
            self.stack.append(token)
            self.stack.append("(")
            for _ in range(self.functions[token].__code__.co_argcount - 1):
                self.stack.append("A")
            self.current_state = "parenthesis"
        elif token.replace(".", "").isalnum():
            if token.isalpha():
                if self.variable_name == "":
                    self.variable_name = token
                else:
                    if token != self.variable_name:
                        return "Error: several names for variable: %s and %s." % (self.variable_name, token)
            if len(self.stack) > 0 and self.stack[-1] == "~":
                self.stack.pop()
            self.current_state = "operator"
        elif token == "~":
            if len(self.stack) > 0 and self.stack[-1] == "~":
                return "Error: two unary '-' found for one operand."
            self.stack.append("~")
        elif token == "(":
            self.stack.append("(")
        else:
            return "Error: expected operand, but '%s' is given." % token

    def __state_parenthesis(self, token):
        if token == "(":
            self.current_state = "operand"
        else:
            return "Error: '(' is expected after a function name, but '%s' is given." % token
