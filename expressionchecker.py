from pda import PDA


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
        print(token_array)
        for i, token in enumerate(token_array):
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
                return "Unbalanced parentheses.", len(token_array) - token_array[::-1].index("(") - 1
            elif self.stack[-1] == "A":
                last_function_name, idx = "", -1
                for i in range(1, len(self.stack) + 1):
                    if self.stack[-i] in self.functions:
                        last_function_name = self.stack[-i]
                        idx = len(self.stack) - i - 1
                        break
                return "Not enough arguments for function %s." % last_function_name, idx
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
                        return "Error: wrong number of arguments for function %s" % self.stack[-2]
                return "Error: unbalanced parentheses."
            elif self.stack[-1] == "A":
                self.stack.pop()
                self.current_state = "operand"
        elif token == ")":
            if len(self.stack) == 0 or self.stack[-1] != "(":
                return "Error: unbalanced parentheses."
            self.stack.pop()
            if len(self.stack) > 0 and self.stack[-1] in self.functions:
                self.stack.pop()
        else:
            return "Error: expected operator, but '%s' is given." % token

    def __state_operand(self, token):
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
                        return "Several names for variable: %s and %s." % (token, self.variable_name)
            if len(self.stack) > 0 and self.stack[-1] == "~":
                self.stack.pop()
            self.current_state = "operator"
        elif token == "~":
            if len(self.stack) > 0 and self.stack[-1] == "~":
                return "Two unary '-' found for one operand."
            self.stack.append("~")
        elif token == "(":
            self.stack.append("(")
        else:
            return "Expected operand, but '%s' is given." % token

    def __state_parenthesis(self, token):
        if token == "(":
            self.current_state = "operand"
        else:
            return "Error: '(' is expected after a function name, but '%s' is given." % token
