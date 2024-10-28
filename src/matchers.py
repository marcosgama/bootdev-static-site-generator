import re

from src.patterns import TextPatterns, BlockPatterns
from src.textnode import TextType


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


def match_block_type(text: str) -> str:
    if re.match(BlockPatterns.HEADER.value, text):
        return "header"
    elif re.match(BlockPatterns.CODE.value, text, re.DOTALL):
        return "code"
    elif re.match(BlockPatterns.QUOTE.value, text, re.DOTALL):
        return "quote"
    elif re.match(BlockPatterns.ULIST.value, text):
        return "ulist"
    elif re.match(BlockPatterns.OLIST.value, text):
        return "olist"
