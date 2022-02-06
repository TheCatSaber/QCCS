import unittest

from context import ComplexMatrix


class ComplexMatrixInitCheck(unittest.TestCase):
    def test_init(self):
        ComplexMatrix()
