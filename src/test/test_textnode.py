import unittest

from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_node = TextNode("hello world", "text", "https://www.google.com")
        text_node2 = TextNode("hello world", "text", "https://www.google.com")
        self.assertEqual(text_node, text_node2)

    def test_not_eq(self):
        text_node_properties = [
            ("hello world", "text", "https://www.google.com"),
            ("hello world", "text", "https://www.facebook.com"),
            ("hello world", "text", "https://www.instagram.com"),
        ]

        other_text_node_properties = [
            ("hello world", None, "https://www.google.com"),
            ("ola mundo", "text", "https://www.facebook.com"),
            ("hello world", "text", "https://instagram.com"),
        ]

        for text_node_property, other_text_node_property in zip(
            text_node_properties, other_text_node_properties
        ):
            text_node = TextNode(*text_node_property)
            text_node2 = TextNode(*other_text_node_property)
            self.assertNotEqual(text_node, text_node2)


if __name__ == "__main__":
    unittest.main()
