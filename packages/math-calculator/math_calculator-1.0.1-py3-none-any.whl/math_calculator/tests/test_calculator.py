import unittest
from math_calculator.calculator import add, subtract, multiply, divide
import emoji

class CalculatorTest(unittest.TestCase):

    def test_add(self):
        result = add(3, 5)
        expected = emoji.emojize(":plus:") + " 8"
        self.assertEqual(result, expected)

    def test_subtract(self):
        result = subtract(10, 4)
        expected = emoji.emojize(":minus:") + " 6"
        self.assertEqual(result, expected)

    def test_multiply(self):
        result = multiply(2, 3)
        expected = emoji.emojize(":multiply:") + " 6"
        self.assertEqual(result, expected)

    def test_divide(self):
        result = divide(10, 2)
        expected = emoji.emojize(":divide:") + " 5.0"
        self.assertEqual(result, expected)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
