import unittest

from src.matchers import match_block_type, match_text_type
from src.textnode import TextType


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


class TestMatchBlockType(unittest.TestCase):
    def setUp(self):
        self.blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "1. Item A\n2. Item B",
            "This is more text **after the ordered lists**. Now text with unordered lists:",
            "* Item A\n* Item B",
            "And more unordered lists",
            "- Item A\n- Item B",
        ]

    def test_match_block_types(self):
        expected = ["header", "paragraph", "olist",
                    "paragraph", "ulist", "paragraph", "ulist"]

        for test_case, expected in zip(self.blocks, expected):
            res = match_block_type(test_case)
            self.assertEqual(res, expected)
