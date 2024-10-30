from src.matchers import match_block_type
from src.delimiters import delimit_nodes
from src.htmlnode import ParentNode, HTMLNode
from src.patterns import TextPatterns
from src.delimiters import delimit_blocks


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(text: str) -> str:
    return match_block_type(text)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = delimit_nodes(
        text,
        patterns=[
            TextPatterns.BOLD.value,
            TextPatterns.CODE.value,
            TextPatterns.IMAGE.value,
            TextPatterns.ITALIC.value,
            TextPatterns.LINK.value,
        ],
    )
    children = []
    for text_node in text_nodes:
        children.append(text_node.to_html())
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    print(text)
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = match_block_type(block)
    match block_type:
        case "paragraph":
            return paragraph_to_html_node(block)
        case "header":
            return heading_to_html_node(block)
        case "code":
            return code_to_html_node(block)
        case "olist":
            return olist_to_html_node(block)
        case "ulist":
            return ulist_to_html_node(block)
        case "quote":
            return quote_to_html_node(block)
        case "_":
            raise ValueError("Invalid block type")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
