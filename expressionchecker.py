from operand import *
from pda import PDA


class ExpressionChecker(PDA):
    def __init__(self, operators, operator_precedences, functions):
        """
        Creates an arithmetic expression checker based on push-down automaton
        It has three states: awaiting operand, awaiting operator and awaiting parenthesis (after function)
        By now supports expressions with only variable
        :param operators: a dictionary (operator_name: string, operator_function: function)
        :param operator_precedences: a dictionary (operator_name: string, operator_priority: int)
        :param functions: a dictionary (function_name: string, function_body: function)
        :return:
        """
        states = {"operator": self.state_operator,
                  "operand": self.state_operand,
                  "parenthesis": self.state_parenthesis}
        super().__init__(states, current_state="operand")

        self.operators = operators
        self.op_precedences = operator_precedences
        self.functions = functions
        self.variable_name = ""

    def state_operator(self, token):
        if token in self.operators:
            self.current_state = "operand"
        elif token == ",":
            if len(self.stack) == 0:
                return "Error: ',' is put out of a function"
            elif self.stack[-1] == "(":
                return "Error: unbalanced parentheses"
            elif self.stack[-1] == "A":
                self.stack.pop()
                self.current_state = "operand"
        elif token == ")":
            if len(self.stack) == 0 or self.stack[-1] != "(":
                return "Error: unbalanced parentheses"
            self.stack.pop()
            if len(self.stack) > 0 and self.stack[-1] in self.functions:
                self.stack.pop()
        else:
            return "Error: expected operator, but '%s' is given" % token

    def state_operand(self, token):
        if token in self.functions:
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
                        return "Several names for variable: %s and %s" % (token, self.variable_name)
            if len(self.stack) > 0 and self.stack[-1] == "~":
                self.stack.pop()
            self.current_state = "operator"
        elif token == "~":
            if len(self.stack) > 0 and self.stack[-1] == "~":
                return "Two unary '-' found for one operand"
            self.stack.append("~")
        elif token == "(":
            self.stack.append("(")
        else:
            return "Expected operand but '%s' is given" % token

    def state_parenthesis(self, token):
        if token == "(":
            self.current_state = "operand"
        else:
            return "Error: '(' expected after function name, but '%s' is given" % token
