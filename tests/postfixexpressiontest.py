import unittest

from operand import Operand
from postfixexpression import PostfixExpression


class PostfixExpressionTest(unittest.TestCase):
    def test_correct_expressions(self):
        expr_1 = PostfixExpression("(a+ 36)/ log(2 , 4)")
        self.assertEqual(expr_1.error_msg, None)
        self.assertEqual(expr_1.error_place, (None, None))
        self.assertEqual(expr_1.interpreted_expression, "(a+36)/log(2,4)")
        self.assertEqual(expr_1.result, Operand([18, 0.5]))

        expr_2 = PostfixExpression("log(log(log(log(log(2, 4), 4), 4), 4), 4)")
        self.assertEqual(expr_2.error_msg, None)
        self.assertEqual(expr_2.error_place, (None, None))
        self.assertEqual(expr_2.interpreted_expression, "log(log(log(log(log(2,4),4),4),4),4)")
        self.assertEqual(expr_2.result, Operand([2]))

        expr_3 = PostfixExpression("3*a+3log(2(1+1), 16)-3a")
        self.assertEqual(expr_3.error_msg, None)
        self.assertEqual(expr_3.error_place, (None, None))
        self.assertEqual(expr_3.interpreted_expression, "3*a+3*log(2*(1+1),16)-3*a")
        self.assertEqual(expr_3.result, Operand([6]))

        expr_4 = PostfixExpression("2    * ( -    3 ) +    6  ( -a)-4*( -   log (2   , 4)      )")
        self.assertEqual(expr_4.error_msg, None)
        self.assertEqual(expr_4.error_place, (None, None))
        self.assertEqual(expr_4.interpreted_expression, "2*(-3)+6*(-a)-4*(-log(2,4))")
        self.assertEqual(expr_4.result, Operand([2, -6]))

    def test_unbalanced_parentheses(self):
        expr_1 = PostfixExpression("a+3(4a-1))")
        self.assertEqual(expr_1.error_msg, "Error: unbalanced parentheses.")
        self.assertEqual(expr_1.interpreted_expression, "a+3*(4*a-1))")
        self.assertEqual(expr_1.error_place, (11, 11))
        self.assertIsNone(expr_1.result)

        expr_2 = PostfixExpression("321log(23, 42))")
        self.assertEqual(expr_2.error_msg, "Error: unbalanced parentheses.")
        self.assertEqual(expr_2.interpreted_expression, "321*log(23,42))")
        self.assertEqual(expr_2.error_place, (14, 14))
        self.assertIsNone(expr_2.result)

        expr_3 = PostfixExpression("((23 + 1)*3")
        self.assertEqual(expr_3.error_msg, "Error: unbalanced parentheses.")
        self.assertEqual(expr_3.interpreted_expression, "((23+1)*3")
        self.assertEqual(expr_3.error_place, (0, 0))
        self.assertIsNone(expr_3.result)

        expr_4 = PostfixExpression("3((log((3+2), 25))")
        self.assertEqual(expr_4.error_msg, "Error: unbalanced parentheses.")
        self.assertEqual(expr_4.interpreted_expression, "3*((log((3+2),25))")
        self.assertEqual(expr_4.error_place, (2, 2))
        self.assertIsNone(expr_4.result)

    def test_logarithm(self):
        expr_1 = PostfixExpression("log(2, -1)")
        self.assertEqual(expr_1.error_msg, "Error: illegal value for logarithm.")
        self.assertEqual(expr_1.interpreted_expression, "log(2,-1)")
        self.assertEqual(expr_1.error_place, (4, 7))
        self.assertIsNone(expr_1.result)

        expr_2 = PostfixExpression("log(-1, -1)")
        self.assertEqual(expr_2.error_msg, "Error: illegal base for logarithm.")
        self.assertEqual(expr_2.interpreted_expression, "log(-1,-1)")
        self.assertEqual(expr_2.error_place, (4, 8))
        self.assertIsNone(expr_2.result)

        expr_3 = PostfixExpression("log(-3, 3)")
        self.assertEqual(expr_3.error_msg, "Error: illegal base for logarithm.")
        self.assertEqual(expr_3.interpreted_expression, "log(-3,3)")
        self.assertEqual(expr_3.error_place, (4, 7))
        self.assertIsNone(expr_3.result)

        expr_4 = PostfixExpression("25log(log(2, 4)-3, 128)")
        self.assertEqual(expr_4.error_msg, "Error: illegal base for logarithm.")
        self.assertEqual(expr_4.interpreted_expression, "25*log(log(2,4)-3,128)")
        self.assertEqual(expr_4.error_place, (7, 20))
        self.assertIsNone(expr_4.result)

    def test_div_by_zero(self):
        expr_1 = PostfixExpression("1/0")
        self.assertEqual(expr_1.error_msg, "Error: division by zero.")
        self.assertEqual(expr_1.interpreted_expression, "1/0")
        self.assertEqual(expr_1.error_place, (0, 2))
        self.assertIsNone(expr_1.result)

        expr_2 = PostfixExpression("log(2, (3-3*1.)/0)")
        self.assertEqual(expr_2.error_msg, "Error: division by zero.")
        self.assertEqual(expr_2.interpreted_expression, "log(2,(3-3*1.)/0)")
        self.assertEqual(expr_2.error_place, (6, 15))
        self.assertIsNone(expr_2.result)

        expr_3 = PostfixExpression("log(12/(log(2,4)-2), 123)")
        self.assertEqual(expr_3.error_msg, "Error: division by zero.")
        self.assertEqual(expr_3.interpreted_expression, "log(12/(log(2,4)-2),123)")
        self.assertEqual(expr_3.error_place, (4, 18))
        self.assertIsNone(expr_3.result)

        expr_4 = PostfixExpression("3/(1000000000(log(log(2,4), 2) - 1))")
        self.assertEqual(expr_4.error_msg, "Error: division by zero.")
        self.assertEqual(expr_4.interpreted_expression, "3/(1000000000*(log(log(2,4),2)-1))")
        self.assertEqual(expr_4.error_place, (0, 33))
        self.assertIsNone(expr_4.result)

        expr_5 = PostfixExpression("3/(0.0000000002-(0.0000000001+0.0000000001))")
        self.assertEqual(expr_5.error_msg, "Error: division by zero.")
        self.assertEqual(expr_5.interpreted_expression, "3/(0.0000000002-(0.0000000001+0.0000000001))")
        self.assertEqual(expr_5.error_place, (0, 43))
        self.assertIsNone(expr_5.result)

if __name__ == "__main__":
    unittest.main()
