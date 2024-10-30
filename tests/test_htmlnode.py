import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            # node 0
            ParentNode("p", [LeafNode("b", "foo")]),
            # node 1
            ParentNode("p", [LeafNode("b", "foo"), LeafNode("b", "bar")]),
            # node 2
            ParentNode("p", [ParentNode("p", [LeafNode("b", "bar")])]),
            # node 3
            ParentNode(
                "p", [ParentNode("p", [ParentNode("p", [LeafNode("b", "bar")])])]),
            # node 4
            ParentNode(
                "p",
                [
                    ParentNode(
                        "p2",
                        [ParentNode("p3", [LeafNode("l1", "leaf"),
                                    LeafNode("l2", "leaf2")])],
                    ),
                    ParentNode("p4", [LeafNode("l3", "leaf3")]),
                ],
            ),
            # node 5
            ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            ),
        ]

    def test_single_child_leaf_node(self):
        expected = "<p><b>foo</b></p>"
        node = self.nodes[0]
        self.assertEqual(node.to_html(), expected)

    def test_multi_child_leaf_node(self):
        expected = "<p><b>foo</b><b>bar</b></p>"
        node = self.nodes[1]
        self.assertEqual(node.to_html(), expected)

    def test_single_child_parent_node(self):
        expected = "<p><p><b>bar</b></p></p>"
        node = self.nodes[2]
        self.assertEqual(node.to_html(), expected)

    def test_multi_child_parent_node(self):
        expected = "<p><p><p><b>bar</b></p></p></p>"
        node = self.nodes[3]
        self.assertEqual(node.to_html(), expected)

    def test_full_tree(self):
        expected = "<p><p2><p3><l1>leaf</l1><l2>leaf2</l2></p3></p2><p4><l3>leaf3</l3></p4></p>"
        node = self.nodes[4]
        self.assertEqual(node.to_html(), expected)

    def test_parent_multiple_leaf(self):
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        node = self.nodes[5]
        self.assertEqual(node.to_html(), expected)


class TestLeafNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            LeafNode("p", "This is a paragraph"),
            LeafNode("p", "This is a paragraph", {
                     "style": "text-align: right"}),
        ]

    def test_to_html(self):
        expected_returns = [
            "<p>This is a paragraph</p>",
            '<p style="text-align: right">This is a paragraph</p>',
        ]

        for node, expected_return in zip(self.nodes, expected_returns):
            self.assertEqual(node.to_html(), expected_return)
