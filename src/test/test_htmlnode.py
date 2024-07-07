import unittest

from src.htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_single_props(self):
        html_node = HtmlNode("div", "hello world", [], {"class": "container"})
        self.assertEqual(html_node.props_to_html(), 'class="container"')

    def test_props_to_html_multiple_props(self):
        html_node = HtmlNode(
            "div", "hello world", [], {"class": "container", "id": "main"}
        )
        self.assertEqual(html_node.props_to_html(), 'class="container" id="main"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        leaf_node = LeafNode(None, "hello world\n", {"class": "container"})
        self.assertEqual(leaf_node.to_html(), "hello world\n")

    def test_to_html_no_value(self):
        leaf_node = LeafNode("div", None, {"class": "container"})
        with self.assertRaises(ValueError):
            leaf_node.to_html()

    def test_to_html_no_props(self):
        leaf_node = LeafNode("div", "hello world", None)
        self.assertEqual(leaf_node.to_html(), "<div>hello world</div>")

    def test_to_html(self):
        leaf_node = LeafNode("div", "hello world", {"class": "container"})
        self.assertEqual(
            leaf_node.to_html(), '<div class="container">hello world</div>'
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode(None, [], {"class": "container"})
            parent_node.to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", [], {"class": "container"})
            parent_node.to_html()

    def test_to_html_only_leaves(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", None),
                LeafNode(None, "Normal text", None),
                LeafNode("i", "italic text", None),
                LeafNode(None, "Normal text", None),
            ],
            None,
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_only_parents(self):
        parent_node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Item 1", None),
                                LeafNode(None, "Item 2", None),
                            ],
                            None,
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode(None, "Item 3", None),
                                LeafNode(None, "Item 4", None),
                            ],
                            None,
                        ),
                    ],
                    None,
                )
            ],
            None,
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><ul><li>Item 1Item 2</li><li>Item 3Item 4</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
