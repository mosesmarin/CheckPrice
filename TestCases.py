# tweeTestCasest.py
# Author: Moises Marin
# Date: December 11, 2017
# Purpose: Run test cases
#
#
import unittest
class CheckNumbers(unittest.TestCase):
    def test_int_float(self):
        self.assertEqual(1,1.0)

if __name__=="__main__":
    unittest.main()