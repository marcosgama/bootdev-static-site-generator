import unittest

from src.htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            HTMLNode(
                props={
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
            ),
            HTMLNode("p", "this is a paragraph"),
            HTMLNode("p", "paragraph", [HTMLNode(), HTMLNode()]),
        ]

    def test_repr(self):
        expected_returns = [
            "HTMLNode(None, None, None, {'href': 'https://www.google.com', 'target': '_blank'})",
            "HTMLNode(p, this is a paragraph, None, None)",
            "HTMLNode(p, paragraph, [HTMLNode(None, None, None, None), HTMLNode(None, None, None, None)], None)",
        ]
        for node, expected_return in zip(self.nodes, expected_returns):
            self.assertEqual(repr(node), expected_return)

    def test_props_to_html(self):
        expected_returns = [
            ' href="https://www.google.com" target="_blank"', "", ""]

        for node, expected_return in zip(self.nodes, expected_returns):
            self.assertEqual(node.props_to_html(), expected_return)
