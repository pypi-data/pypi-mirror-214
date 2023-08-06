import unittest
from math_calculator.calculator import add, subtract, multiply, divide
import emoji

class CalculatorTest(unittest.TestCase):

    def test_add(self):
        result = add(3, 5)
        expected = emoji.emojize(":heavy_plus_sign:") + " 8"
        self.assertEqual(result, expected)

    def test_subtract(self):
        result = subtract(10, 4)
        expected = emoji.emojize(":heavy_minus_sign:") + " 6"
        self.assertEqual(result, expected)

    def test_multiply(self):
        result = multiply(2, 3)
        expected = emoji.emojize(":heavy_multiplication_x:") + " 6"
        self.assertEqual(result, expected)

    def test_divide(self):
        result = divide(10, 2)
        expected = emoji.emojize(":heavy_division_sign:") + " 5.0"
        self.assertEqual(result, expected)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
