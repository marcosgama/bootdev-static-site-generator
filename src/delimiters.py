import re

from src.textnode import TextNode, TextType
from src.matchers import match_text_type, match_block_type


def delimit_inline_nodes(text: str, patterns=list[str]) -> list[TextNode]:
    combined_pattern = "|".join(f"({p})" for p in patterns)
    nodes = []
    for m in re.finditer(combined_pattern, text):
        group = filter(lambda group: group is not None, m.groups())
        match list(group):
            case group_pattern, group_text, url:
                nodes.append(TextNode(group_text, match_text_type(group_pattern), m.span(), url))
            case group_pattern, group_text:
                nodes.append(TextNode(group_text, match_text_type(group_pattern), m.span()))

    return nodes


def delimit_text_nodes(text: str, inline_nodes: list[TextNode]) -> list[TextNode]:
    inline_nodes = sorted(inline_nodes)
    text_nodes = []
    if inline_nodes[0][0] > 0:
        beginning = text[0 : inline_nodes[0].span.start]
        text_nodes.append(TextNode(beginning, TextType.TEXT, span=(0, inline_nodes[0].span.start)))

    # check if there is in between text between nodes
    for i in range(0, len(inline_nodes)):
        if i + 1 < len(inline_nodes):
            lower_bound = inline_nodes[i].span.end
            upper_bound = inline_nodes[i + 1].span.start
            if upper_bound > lower_bound:
                text_nodes.append(
                    TextNode(text[lower_bound:upper_bound], TextType.TEXT, span=(lower_bound, upper_bound))
                )

    if inline_nodes[-1][1] < len(text):
        text_nodes.append(
            TextNode(text[inline_nodes[-1][1] :], TextType.TEXT, span=(inline_nodes[-1][1] + 1, len(text)))
        )

    return text_nodes


def delimit_nodes(text: str, patterns=list[str]) -> list[TextNode]:
    inline_nodes = delimit_inline_nodes(text, patterns)
    text_nodes = delimit_text_nodes(text, inline_nodes)
    return sorted(inline_nodes + text_nodes)


def delimit_blocks(text: str, pattern: str) -> list[str]:
    return list(filter(lambda x: x != "", re.split(pattern, text.strip())))
