# test_module.py

import unittest
from excalibur007001.module import greet, add_numbers, factorial

class TestMyPackage(unittest.TestCase):

    def test_greet(self):
        """Test the greet function."""
        self.assertEqual(greet("Alice"), "Hello, Alice! Welcome to my_package.")
        self.assertEqual(greet("Bob"), "Hello, Bob! Welcome to my_package.")

    def test_add_numbers(self):
        """Test the add_numbers function."""
        self.assertEqual(add_numbers(5, 7), 12)
        self.assertEqual(add_numbers(-5, 5), 0)
        self.assertEqual(add_numbers(0, 0), 0)

    def test_factorial(self):
        """Test the factorial function."""
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)

if __name__ == "__main__":
    unittest.main()