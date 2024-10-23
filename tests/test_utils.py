import unittest

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType
from src.utils import (
    text_node_to_html_node,
    split_node_delimiter,
    split_node_delimiters,
    find_delimiter,
    match_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)


class TestNodeToHTMLNode(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            TextNode("bar", TextType("text"), None),
            TextNode("foo", TextType("bold"), None),
            TextNode("foobar", TextType("italic"), None),
            TextNode("print(hello world)", TextType("code"), None),
            TextNode(None, TextType("link"), "https://www.boot.dev"),
            TextNode("img alt text", TextType("image"), "https://www.boot.dev"),
        ]

    def test_text_node_to_html_node(self):
        expected = [
            LeafNode(None, "bar", None),
            LeafNode("b", "foo", None),
            LeafNode("i", "foobar", None),
            LeafNode("code", "print(hello world)", None),
            LeafNode("a", None, {"href": "https://www.boot.dev"}),
            LeafNode("img", "", {"src": "https://www.boot.dev", "alt": "img alt text"}),
        ]
        for node, test_case in zip(self.nodes, expected):
            self.assertEqual(text_node_to_html_node(node), test_case)


class TextNodeDelimiter(unittest.TestCase):
    def test_find_delimiter(self):
        test_text = ["this is **italic**", "this is *bold*", "this is `a code block`"]

        expected = ["**", "*", "`"]

        for test, exp in zip(test_text, expected):
            self.assertEqual(find_delimiter(test), exp)

    def test_match_delimiter(self):
        delimiters = ["**", "*", "`", "-"]
        expected = [TextType.ITALIC, TextType.BOLD, TextType.CODE]

        for test, exp in zip(delimiters, expected):
            if test != "-":
                self.assertEqual(match_delimiter(test), exp)
            self.assertRaises(ValueError)

    def test_split_node_delimiter(self):
        node = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is plain text with no delimiter", TextType.TEXT),
        ]
        expected = [
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            TextNode("This is plain text with no delimiter", TextType.TEXT),
        ]

        for test, exp in zip(node, expected):
            self.assertEqual(split_node_delimiter(test), exp)

    def test_split_node_delimiter_list_of_nodes(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a **italic block** word", TextType.TEXT),
            TextNode("This is text with a *bold block* word", TextType.TEXT),
            TextNode("This is plain text with no delimiters", TextType.TEXT),
        ]

        expected = [
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            TextNode("This is plain text with no delimiters", TextType.TEXT),
        ]
        self.assertEqual(split_node_delimiters(nodes), expected)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_not_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_not_extract_unrelated_text(self):
        cases = [
            "This is some text (in parenthesis)",
            "This is some text [in braces]",
            "This is some text (in parenthesis) and [in braces]",
        ]

        expected = []
        for case in cases:
            self.assertEqual(extract_markdown_images(case), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_not_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_not_extract_unrelated_text(self):
        cases = [
            "This is some text (in parenthesis)",
            "This is some text [in braces]",
            "This is some text (in parenthesis) and [in braces]",
        ]

        expected = []
        for case in cases:
            self.assertEqual(extract_markdown_links(case), expected)
