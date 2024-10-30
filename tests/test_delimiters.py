import unittest

from src.textnode import TextNode, TextType
from src.patterns import TextPatterns, BlockPatterns
from src.delimiters import (
    delimit_text_nodes,
    delimit_inline_nodes,
    delimit_nodes,
    delimit_blocks,
)


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
            TextNode("obi wan image", TextType.IMAGE, (65, 115), "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, (122, 146), "https://boot.dev"),
        ]
        self.assertEqual(delimit_inline_nodes(self.test_text, self.patterns), expected)

    def test_delimit_text_nodes(self):
        inline_nodes = delimit_inline_nodes(self.test_text, patterns=self.patterns)

        expected = [
            TextNode("This is ", TextType.TEXT, (0, 8)),
            TextNode(" with an ", TextType.TEXT, (16, 25)),
            TextNode(" word and a ", TextType.TEXT, (33, 45)),
            TextNode(" and an ", TextType.TEXT, (57, 65)),
            TextNode(" and a ", TextType.TEXT, (115, 122)),
            TextNode(" and some more text", TextType.TEXT, (147, 165)),
        ]

        self.assertEqual(delimit_text_nodes(self.test_text, inline_nodes), expected)

    def test_delimit_nodes(self):
        expected = [
            TextNode("This is ", TextType.TEXT, (0, 8)),
            TextNode("text", TextType.BOLD, (8, 16)),
            TextNode(" with an ", TextType.TEXT, (16, 25)),
            TextNode("italic", TextType.ITALIC, (25, 33)),
            TextNode(" word and a ", TextType.TEXT, (33, 45)),
            TextNode("code block", TextType.CODE, (45, 57)),
            TextNode(" and an ", TextType.TEXT, (57, 65)),
            TextNode("obi wan image", TextType.IMAGE, (65, 115), "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT, (115, 122)),
            TextNode("link", TextType.LINK, (122, 146), "https://boot.dev"),
            TextNode(" and some more text", TextType.TEXT, (147, 165)),
        ]
        self.assertEqual(delimit_nodes(self.test_text, self.patterns), expected)


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
