import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType
from src.patterns import TextPatterns, BlockPatterns
from src.splitters import (
    text_node_to_html_node,
    match_text_type,
    delimit_text_nodes,
    delimit_inline_nodes,
    delimit_nodes,
    delimit_blocks,
)


class TestNodeToHTMLNode(unittest.TestCase):
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
            self.assertEqual(text_node_to_html_node(node), test_case)


class TestMatchTextType(unittest.TestCase):
    def test_match_text_type(self):
        test_case = ["*foo*", "**foo**", "`foo`", "[foo]", "![foo]"]

        expected = [TextType.ITALIC, TextType.BOLD,
                    TextType.CODE, TextType.LINK, TextType.IMAGE]

        for text, expected in zip(test_case, expected):
            self.assertEqual(match_text_type(text), expected)

    def test_fails_unknown_delimiter(self):
        test_case = "$foo$"
        self.assertRaises(ValueError, match_text_type, test_case)


class TestDelimitNodes(unittest.TestCase):
    def setUp(self):
        self.test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and some more text"
        self.patterns = [
            TextPatterns.BOLD.value,
            TextPatterns.CODE.value,
            TextPatterns.ITALIC.value,
            TextPatterns.LINK.value,
            TextPatterns.IMAGE.value,
        ]

    def test_delimit_inline_nodes(self):
        expected = [
            TextNode("text", TextType.BOLD, (8, 16)),
            TextNode("italic", TextType.ITALIC, (25, 33)),
            TextNode("code block", TextType.CODE, (45, 57)),
            TextNode("obi wan image", TextType.IMAGE, (65, 115),
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, (122, 146), "https://boot.dev"),
        ]
        self.assertEqual(delimit_inline_nodes(
            self.test_text, self.patterns), expected)

    def test_delimit_text_nodes(self):
        inline_nodes = delimit_inline_nodes(
            self.test_text, patterns=self.patterns)

        expected = [
            TextNode("This is ", TextType.TEXT, (0, 8)),
            TextNode(" with an ", TextType.TEXT, (16, 25)),
            TextNode(" word and a ", TextType.TEXT, (33, 45)),
            TextNode(" and an ", TextType.TEXT, (57, 65)),
            TextNode(" and a ", TextType.TEXT, (115, 122)),
            TextNode(" and some more text", TextType.TEXT, (147, 165)),
        ]

        self.assertEqual(delimit_text_nodes(
            self.test_text, inline_nodes), expected)

    def test_delimit_nodes(self):
        expected = [
            TextNode("This is ", TextType.TEXT, (0, 8)),
            TextNode("text", TextType.BOLD, (8, 16)),
            TextNode(" with an ", TextType.TEXT, (16, 25)),
            TextNode("italic", TextType.ITALIC, (25, 33)),
            TextNode(" word and a ", TextType.TEXT, (33, 45)),
            TextNode("code block", TextType.CODE, (45, 57)),
            TextNode(" and an ", TextType.TEXT, (57, 65)),
            TextNode("obi wan image", TextType.IMAGE, (65, 115),
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, (115, 122)),
            TextNode("link", TextType.LINK, (122, 146), "https://boot.dev"),
            TextNode(" and some more text", TextType.TEXT, (147, 165)),
        ]
        self.assertEqual(delimit_nodes(
            self.test_text, self.patterns), expected)


class TestDelimitBlocks(unittest.TestCase):
    def setUp(self):
        self.text = r"""   # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

1. Item A
2. Item B

This is more text **after the ordered lists**. Now text with unordered lists:

* Item A
* Item B

And more unordered lists

- Item A
- Item B
    """

    def test_block_delimiter(self):
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "\n1. Item A\n2. Item B",
            "This is more text **after the ordered lists**. Now text with unordered lists:",
            "\n* Item A\n* Item B",
            "And more unordered lists",
            "\n- Item A\n- Item B",
        ]

        self.assertEqual(delimit_blocks(
            self.text, TextPatterns.BLOCK.value), expected)
