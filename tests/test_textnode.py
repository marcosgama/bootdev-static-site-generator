import unittest
from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_equality(self):
        node1 = TextNode("foo", "bar", "foobar")
        node2 = TextNode("foo", "bar", "foobar")
        self.assertEqual(node1, node2)

    def test_inequality(self):
        base_case = TextNode("foo", "bar", "foobar")
        test_cases = (
            TextNode("bar", "bar", "foobar"),
            TextNode("foo", "foo", "foobar"),
            TextNode("foo", "bar", "barfoo"),
            TextNode("foo", "bar"),
        )
        for case in test_cases:
            self.assertNotEqual(case, base_case)
