import unittest
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [TextNode("foo", TextType("bold")), TextNode("foo", TextType("italic"), "https://boot.dev")]

    def test_equality(self):
        test_nodes = [TextNode("foo", TextType("bold")), TextNode("foo", TextType("italic"), "https://boot.dev")]

        for node, test_node in zip(self.nodes, test_nodes):
            self.assertEqual(node, test_node)

    def test_inequality(self):
        test_nodes = (
            TextNode("bar", TextType("bold")),
            TextNode("foo", TextType("italic")),
        )
        for node, test_node in zip(self.nodes, test_nodes):
            self.assertNotEqual(node, test_node)

    def test_repr(self):
        test_nodes = ["TextNode(foo, bold, None)", "TextNode(foo, italic, https://boot.dev)"]

        for node, test_node in zip(self.nodes, test_nodes):
            self.assertEqual(repr(node), test_node)
