import unittest

from operand import Operand


class OperandTest(unittest.TestCase):
    def test_add_eq_length(self):
        op_1 = Operand([1, 2, 3])
        op_2 = Operand([4, 5, 6])
        result = Operand([5, 7, 9])
        self.assertEqual(op_1 + op_2, result)

    def test_add_neq_length(self):
        op_1 = Operand([1, 2, 3])
        op_2 = Operand([4, 5, 6, 0, 3])
        result = Operand([5, 7, 9, 0, 3])
        self.assertEqual(op_1 + op_2, result)

    def test_sub_eq_length(self):
        op_1 = Operand([1, 2, 3])
        op_2 = Operand([4, 5, 6])
        result = Operand([-3, -3, -3])
        self.assertEqual(op_1 - op_2, result)

    def test_sub_neq_length(self):
        op_1 = Operand([1, 2, 3])
        op_2 = Operand([4, 5, 6, 0, 3])
        result = Operand([-3, -3, -3, 0, -3])
        self.assertEqual(op_1 - op_2, result)

    def test_mul(self):
        op_1 = Operand([2, 3])
        op_2 = Operand([0, 4, 2])
        result = Operand([0, 8, 16, 6])
        self.assertEqual(op_1 * op_2, result)

    def test_div_trivial(self):
        op_1 = Operand([0, 3, 3])
        op_2 = Operand([3])
        result = Operand([0, 1, 1])
        self.assertEqual(op_1 / op_2, result)

    def test_div(self):
        op_1 = Operand([0, 3, 3])
        op_2 = Operand([3, 3])
        result = Operand([0, 1])
        self.assertEqual(op_1 / op_2, result)

if __name__ == "__main__":
    unittest.main()