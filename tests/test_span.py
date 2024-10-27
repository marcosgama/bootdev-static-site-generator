import unittest
from src.textnode import Span


class TestSpan(unittest.TestCase):
    def test_raise_when_less_than_zero(self):
        self.assertRaises(ValueError, Span, -1, 0)
        self.assertRaises(ValueError, Span, 0, -1)

    def test_compares_with_tuple(self):
        self.assertTrue(Span(0, 1) == tuple([0, 1]))
        self.assertTrue(Span(1, 1) > tuple([0, 1]))
        self.assertTrue(Span(0, 1) < tuple([1, 1]))

    def test_fails_instance_more_two_args(self):
        self.assertRaises(TypeError, Span, 1, 2, 3)
