import unittest
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            TextNode("foo", TextType("bold"), (0, 1)),
            TextNode("foo", TextType("italic"), (0, 1), "https://boot.dev"),
        ]

    def test_equality(self):
        test_nodes = [
            TextNode("foo", TextType("bold"), (0, 1)),
            TextNode("foo", TextType("italic"), (0, 1), "https://boot.dev"),
        ]

        for node, test_node in zip(self.nodes, test_nodes):
            self.assertEqual(node, test_node)

    def test_inequality(self):
        test_nodes = (
            TextNode("bar", TextType("bold"), (0, 1)),
            TextNode("foo", TextType("italic"), (0, 1)),
        )

        for node, test_node in zip(self.nodes, test_nodes):
            self.assertNotEqual(node, test_node)

    def test_repr(self):
        test_nodes = [
            "TextNode(foo, bold, Span(start=0, end=1), None)",
            "TextNode(foo, italic, Span(start=0, end=1), https://boot.dev)",
        ]

        for node, test_node in zip(self.nodes, test_nodes):
            self.assertEqual(repr(node), test_node)
