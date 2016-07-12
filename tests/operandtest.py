import unittest

from operand import Operand


class OperandTest(unittest.TestCase):
    def test_constructor(self):
        op_0 = Operand([0, 0, 0, 0, 1])
        op_1 = Operand([0, 0, 0, 0])
        op_2 = Operand([0, 0, 0])
        op_3 = Operand([0, 0])
        op_4 = Operand([0])
        self.assertNotEqual(op_0, op_1)
        self.assertEqual(op_1, op_2)
        self.assertEqual(op_2, op_3)
        self.assertEqual(op_4, op_4)

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

    def test_add_res_zero(self):
        op_1 = Operand([0, -3])
        op_2 = Operand([0, 3])
        result = Operand([0])
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

    def test_sub_res_zero(self):
        op_1 = Operand([0, 0, 0, 0, 3])
        op_2 = Operand([0, 0, 0, 0, 3])
        result = Operand([0])
        self.assertEqual(op_1 - op_2, result)

    def test_mul(self):
        op_1 = Operand([2, 3])
        op_2 = Operand([0, 4, 2])
        result = Operand([0, 8, 16, 6])
        self.assertEqual(op_1 * op_2, result)

    def test_mul_res_zero(self):
        op_1 = Operand([0])
        op_2 = Operand([1, 2, 3, 4])
        result = Operand([0])
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

    def test_div_by_zero(self):
        op_1 = Operand([1])
        op_2 = Operand([0])
        with self.assertRaises(ZeroDivisionError):
            op_1 / op_2

    def test_div_neg(self):
        op_1 = Operand([1])
        op_2 = Operand([0, 1])
        with self.assertRaises(NotImplementedError):
            op_1 / op_2

    def test_log_polynomial(self):
        op_1 = Operand([0, 1])
        op_2 = Operand([2])
        with self.assertRaises(NotImplementedError):
            op_1.log(op_2)

        with self.assertRaises(NotImplementedError):
            op_2.log(op_1)

    def test_log(self):
        op_1 = Operand([2.71828])
        op_2 = Operand([7.35928])
        self.assertAlmostEqual(op_2.log(op_1).polynomial[0], 2, places=2)

    def test_varstring(self):
        op_0 = Operand([1, 2])
        op_1 = Operand([1., 2.])
        result = "1 + 2a"
        self.assertEqual(op_0.varstring("a"), result)
        self.assertEqual(op_0.varstring("a"), op_1.varstring("a"))

if __name__ == "__main__":
    unittest.main()
