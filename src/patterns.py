from enum import Enum


class TextPatterns(Enum):
    BOLD = r"\*\*(?!\*)(.*?)\*\*"
    CODE = r"\`(.*?)\`"
    IMAGE = r"!\[(.*?)\]\((.*?)\)"
    ITALIC = r"(?<!\*)\*(?!\*)(.*?)\*(?!\*)"
    LINK = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    BLOCK = r"\n(?![*\-+]\s|\d+\. )"


# TODO OLIST and ULIST need to handle indentation
class BlockPatterns(Enum):
    HEADER = r"^#{1,6}.+"
    CODE = r"^`{3}.+"
    QUOTE = r"^>+ .+"
    OLIST = r"^\s*\d. .+"
    ULIST = r"^\s*-|"
