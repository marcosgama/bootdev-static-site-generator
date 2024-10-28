import re
from src.textnode import TextNode, TextType, Patterns
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


def match_text_type(text: str) -> TextType:
    if "**" in text:
        return TextType.BOLD
    elif "*" in text:
        return TextType.ITALIC
    elif "`" in text:
        return TextType.CODE
    elif "![" in text:
        return TextType.IMAGE
    elif "[" in text:
        return TextType.LINK
    else:
        raise ValueError("No valid delimiter found")


def delimit_inline_nodes(text: str, patterns=list[str]) -> list[TextNode]:
    combined_pattern = "|".join(f"({p})" for p in patterns)
    nodes = []
    for m in re.finditer(combined_pattern, text):
        group = filter(lambda group: group is not None, m.groups())
        match list(group):
            case group_pattern, group_text, url:
                nodes.append(TextNode(group_text, match_text_type(
                    group_pattern), m.span(), url))
            case group_pattern, group_text:
                nodes.append(
                    TextNode(group_text, match_text_type(group_pattern), m.span()))

    return nodes


def delimit_text_nodes(text: str, inline_nodes: list[TextNode]) -> list[TextNode]:
    inline_nodes = sorted(inline_nodes)
    text_nodes = []
    if inline_nodes[0][0] > 0:
        beginning = text[0: inline_nodes[0].span.start]
        text_nodes.append(TextNode(beginning, TextType.TEXT,
                          span=(0, inline_nodes[0].span.start)))

    # check if there is in between text between nodes
    for i in range(0, len(inline_nodes)):
        if i + 1 < len(inline_nodes):
            lower_bound = inline_nodes[i].span.end
            upper_bound = inline_nodes[i + 1].span.start
            if upper_bound > lower_bound:
                between = (lower_bound, upper_bound)
                text_nodes.append(
                    TextNode(text[between[0]: between[1]], TextType.TEXT, span=between))

    if inline_nodes[-1][1] < len(text):
        text_nodes.append(
            TextNode(text[inline_nodes[-1][1]:], TextType.TEXT,
                     span=(inline_nodes[-1][1] + 1, len(text)))
        )

    return text_nodes


def delimit_nodes(text: str, patterns=list[str]) -> list[TextNode]:
    inline_nodes = delimit_inline_nodes(text, patterns)
    text_nodes = delimit_text_nodes(text, inline_nodes)
    return sorted(inline_nodes + text_nodes)


def delimit_blocks(text: str, pattern: str) -> list[str]:
    return list(filter(lambda x: x != "", re.split(pattern, text.strip())))
