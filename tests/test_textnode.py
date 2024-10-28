import unittest

from src.textnode import TextNode, TextType
from src.htmlnode import LeafNode


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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            TextNode("bar", TextType("text"), (0, 1), None),
            TextNode("foo", TextType("bold"), (0, 1), None),
            TextNode("foobar", TextType("italic"), (0, 1), None),
            TextNode("print(hello world)", TextType("code"), (0, 1), None),
            TextNode(None, TextType("link"), (0, 1), "https://www.boot.dev"),
            TextNode("img alt text", TextType("image"),
                     (0, 1), "https://www.boot.dev"),
        ]

    def test_text_node_to_html_node(self):
        expected = [
            LeafNode(None, "bar", None),
            LeafNode("b", "foo", None),
            LeafNode("i", "foobar", None),
            LeafNode("code", "print(hello world)", None),
            LeafNode("a", None, {"href": "https://www.boot.dev"}),
            LeafNode(
                "img", "", {"src": "https://www.boot.dev", "alt": "img alt text"}),
        ]
        for node, test_case in zip(self.nodes, expected):
            self.assertEqual(node.to_html(), test_case)
