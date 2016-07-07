import random
import unittest

from solver import *


class SolverTest(unittest.TestCase):
    def testCase_1(self):
        solver = Solver()
        input_string = "(3+(4-1))*5"
        exp_output = "30"
        self.assertEqual(solver.evaluate_infix(input_string), exp_output)

    def testCase_2(self):
        solver = Solver()
        input_string = "2 * x + 0.5 = 1"
        exp_output = "x = 0.25"
        self.assertEqual(solver.evaluate_infix(input_string), exp_output)

    def testCase_3(self):
        solver = Solver()
        input_string = "2x + 1 = 2(1-x)"
        exp_output = "x = 0.25"
        self.assertEqual(solver.evaluate_infix(input_string), exp_output)

    def testCase_4(self):
        solver = Solver()
        strlen = random.randint(0, 30)
        possible_chars = list("1234567890-+=*/.,()logn")
        for i in range(100000):
            random_string = ''.join(random.choice(possible_chars) for _ in range(strlen))
            print(random_string)
            solver.evaluate_infix(random_string)
        self.assertTrue(True)
