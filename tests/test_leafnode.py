import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            LeafNode("p", "This is a paragraph"),
            LeafNode("p", "This is a paragraph", {"style": "text-align: right"}),
        ]

    def test_to_html(self):
        expected_returns = [
            "<p>This is a paragraph</p>",
            '<p style="text-align: right">This is a paragraph</p>',
        ]

        for node, expected_return in zip(self.nodes, expected_returns):
            self.assertEqual(node.to_html(), expected_return)
