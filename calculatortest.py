import random
import unittest

from calculator import evaluate_infix


class CalculatorTest(unittest.TestCase):
    def testCase_1(self):
        input_string = "(3+(4-1))*5"
        exp_output = None, None, "30"
        self.assertEqual(evaluate_infix(input_string), exp_output)

    def testCase_2(self):
        input_string = "2 * x + 0.5 = 1"
        exp_output = None, None, "x = 0.25"
        self.assertEqual(evaluate_infix(input_string), exp_output)

    def testCase_3(self):
        input_string = "2x + 1 = 2(1-x)"
        exp_output = None, None, "x = 0.25"
        self.assertEqual(evaluate_infix(input_string), exp_output)

    def testCase_4(self):
        strlen = random.randint(0, 30)
        possible_chars = list("1234567890-+=*/.,()logn")
        for i in range(100000):
            random_string = ''.join(random.choice(possible_chars) for _ in range(strlen))
            print(random_string)
            evaluate_infix(random_string)
        self.assertTrue(True)
