import re
from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unsupported text type")


def find_delimiter(text: str) -> str:
    if "**" in text:
        return "**"
    elif "*" in text:
        return "*"
    elif "`" in text:
        return "`"


def match_delimiter(delimiter: str) -> TextType:
    if delimiter == "**":
        return TextType.ITALIC
    elif delimiter == "*":
        return TextType.BOLD
    elif delimiter == "`":
        return TextType.CODE
    else:
        ValueError("No valid delimiter found")


def split_node_delimiter(node: TextNode) -> list[TextNode]:
    if node.text_type == TextType.TEXT:
        delimiter = find_delimiter(node.text)
        if delimiter:
            text_type = match_delimiter(delimiter)
            pre, middle, post = node.text.split(delimiter)
            return [TextNode(pre, TextType.TEXT), TextNode(middle, text_type), TextNode(post, TextType.TEXT)]
        return node


def split_node_delimiters(nodes: list[TextNode]) -> list[list[TextNode]]:
    return list(map(split_node_delimiter, nodes))


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
