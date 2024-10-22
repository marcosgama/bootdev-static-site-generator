import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType
from src.utils import text_node_to_html_node


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            TextNode("bar", TextType("text"), None),
            TextNode("foo", TextType("bold"), None),
            TextNode("foobar", TextType("italic"), None),
            TextNode("print(hello world)", TextType("code"), None),
            TextNode(None, TextType("link"), "https://www.boot.dev"),
            TextNode("img alt text", TextType(
                "image"), "https://www.boot.dev"),
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
            self.assertEqual(text_node_to_html_node(node), test_case)
