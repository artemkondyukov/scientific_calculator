import math
import unittest

from expressionchecker import ExpressionChecker
from operand import Operand

operators = {"+": lambda x, y: x + y,
             "-": lambda x, y: x - y,
             "*": lambda x, y: x * y,
             "/": lambda x, y: x / y,
             "~": lambda x: Operand([0]) - x}  # Unary '-' operator

functions = {"log": lambda x, y: y.log(x),
             "ln": lambda x: x.log(Operand([math.e]))}


class ExpressionCheckerTest(unittest.TestCase):
    def test_correct_expressions(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["x", "+", "12", "-", "3", "*", "(", "25", "+", "x", ")"]
        expr_2 = ["~", "3", "-", "4", "-", "5", "-", "6", "*", "(", "x", "+", "(", "~", "3", ")", ")"]
        expr_3 = ["log", "(", "2", ",", "4", ")"]
        self.assertEqual(checker.consume_token_array(expr_1), (None, None))
        self.assertEqual(checker.consume_token_array(expr_2), (None, None))
        self.assertEqual(checker.consume_token_array(expr_3), (None, None))

    def test_unbalanced_parentheses(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["2", "*", "(", "3"]
        self.assertEqual(checker.consume_token_array(expr_1), ("Error: unbalanced parentheses.", 2))
        expr_2 = ["2", "+", "(", "2", "-", "(", "3", "+", "4", ")"]
        self.assertEqual(checker.consume_token_array(expr_2), ("Error: unbalanced parentheses.", 2))
        expr_3 = ["3", "*", "(", "log", "(", "2", ",", "4", ")", "+", "1"]
        self.assertEqual(checker.consume_token_array(expr_3), ("Error: unbalanced parentheses.", 2))

    def test_several_varnames(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["a", "+", "b", "-", "1"]
        self.assertEqual(checker.consume_token_array(expr_1), ("Error: several names for variable: a and b.", 2))
        expr_2 = ["log", "(", "2", ",", "a", ")", "+", "(", "b"]
        self.assertEqual(checker.consume_token_array(expr_2), ("Error: several names for variable: a and b.", 8))

    def test_two_unary_minus(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["~", "~", "b", "-", "1"]
        self.assertEqual(checker.consume_token_array(expr_1), ("Error: two unary '-' found for one operand.", 1))
        expr_2 = ["log", "(", "~", "~", "1"]
        self.assertEqual(checker.consume_token_array(expr_2), ("Error: two unary '-' found for one operand.", 3))
        expr_3 = ["~", "~", "log"]
        self.assertEqual(checker.consume_token_array(expr_3), ("Error: two unary '-' found for one operand.", 1))

    def test_end_of_string(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["log"]
        self.assertEqual(checker.consume_token_array(expr_1),
                         ("Error: '(' is expected after a function name, but the end of the expression reached.", -1))
        expr_2 = ["3", "+"]
        self.assertEqual(checker.consume_token_array(expr_2),
                         ("Error: operand is expected, but the end of the expression reached.", -1))
        expr_3 = ["3", "+", "log", "("]
        self.assertEqual(checker.consume_token_array(expr_3),
                         ("Error: operand is expected, but the end of the expression reached.", -1))

    def test_expected_operand(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = [")"]
        self.assertEqual(checker.consume_token_array(expr_1), ("Error: expected operand, but ')' is given.", 0))
        expr_2 = ["log", "(", ")"]
        self.assertEqual(checker.consume_token_array(expr_2), ("Error: expected operand, but ')' is given.", 2))
        expr_3 = ["2", "+", "+"]
        self.assertEqual(checker.consume_token_array(expr_3), ("Error: expected operand, but '+' is given.", 2))
        expr_4 = ["~", ")"]
        self.assertEqual(checker.consume_token_array(expr_4), ("Error: expected operand, but ')' is given.", 1))
        expr_5 = ["312", "*", "log", "(", "123", ",", "~", "+"]
        self.assertEqual(checker.consume_token_array(expr_5), ("Error: expected operand, but '+' is given.", 7))
        expr_6 = ["312", "*", "."]
        self.assertEqual(checker.consume_token_array(expr_6), ("Error: expected operand, but '.' is given.", 2))
        expr_7 = ["3", "*", ","]
        self.assertEqual(checker.consume_token_array(expr_7), ("Error: expected operand, but ',' is given.", 2))

    def test_expected_operator(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["3", ","]
        self.assertEqual(checker.consume_token_array(expr_1), ("Error: ',' is put out of a function.", 1))
        expr_2 = ["3", "*", "(", "12", ",", "24", ")"]
        self.assertEqual(checker.consume_token_array(expr_2), ("Error: ',' is put out of a function.", 4))
        expr_3 = ["3", "*", "log", "(", "2", ",", "8", ")", ","]
        self.assertEqual(checker.consume_token_array(expr_3), ("Error: ',' is put out of a function.", 8))
        expr_4 = ["3", "*", "log", "(", "2", "+", "(", "3", ",", "2", ")" ",", "8", ")", ","]
        self.assertEqual(checker.consume_token_array(expr_4), ("Error: ',' is put out of a function.", 8))
        expr_5 = ["3", "*", "log", "(", "2", ",", "3", ",", "4", ")"]
        self.assertEqual(checker.consume_token_array(expr_5), ("Error: wrong number of arguments for function log.", 7))
        expr_6 = ["3", "*", "log", "(", "2", ")"]
        self.assertEqual(checker.consume_token_array(expr_6), ("Error: wrong number of arguments for function log.", 5))
        expr_7 = ["3", "*", "ln", "(", "2", ",", "3", ")"]
        self.assertEqual(checker.consume_token_array(expr_7), ("Error: wrong number of arguments for function ln.", 5))
        expr_8 = ["3", "+", "1", ")"]
        self.assertEqual(checker.consume_token_array(expr_8), ("Error: unbalanced parentheses.", 3))
        expr_9 = ["3", "+", "(", "2", "+", "log", "(", "2", ",", "4", ")", ")", ")"]
        self.assertEqual(checker.consume_token_array(expr_9), ("Error: unbalanced parentheses.", 12))
        expr_10 = ["3", "3"]
        self.assertEqual(checker.consume_token_array(expr_10), ("Error: expected operator, but '3' is given.", 1))
        expr_11 = ["3", "*", "(", "a", "+", "1", ")", "("]
        self.assertEqual(checker.consume_token_array(expr_11), ("Error: expected operator, but '(' is given.", 7))
        expr_12 = ["3", "log"]
        self.assertEqual(checker.consume_token_array(expr_12), ("Error: expected operator, but 'log' is given.", 1))

    def test_unallowed_characters(self):
        checker = ExpressionChecker(operators=operators, functions=functions)
        expr_1 = ["321", "+", "`", "1"]
        expr_2 = ["\0"]
        expr_3 = ["a\x03", "\0"]
        expr_4 = ["123", "\0+\0"]
        with self.assertRaises(ValueError):
            checker.consume_token_array(expr_1)
        with self.assertRaises(ValueError):
            checker.consume_token_array(expr_2)
        with self.assertRaises(ValueError):
            checker.consume_token_array(expr_3)
        with self.assertRaises(ValueError):
            checker.consume_token_array(expr_4)

if __name__ == "__main__":
    unittest.main()
