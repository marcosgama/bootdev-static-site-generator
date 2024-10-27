from enum import Enum


class Patterns(Enum):
    BOLD = r"\*\*(?!\*)(.*?)\*\*"
    CODE = r"\`(.*?)\`"
    IMAGE = r"!\[(.*?)\]\((.*?)\)"
    ITALIC = r"(?<!\*)\*(?!\*)(.*?)\*(?!\*)"
    LINK = r"(?<!\!)\[(.*?)\]\((.*?)\)"


class TextType(Enum):
    BOLD = "bold"
    CODE = "code"
    ITALIC = "italic"
    IMAGE = "image"
    LINK = "link"
    TEXT = "text"


class Span(tuple):
    def __new__(cls, start: int, end: int) -> None:
        if start < 0 or end < 0:
            raise ValueError("Args must be >= 0")

        instance = super(Span, cls).__new__(cls, [start, end])
        instance.start = start
        instance.end = end

        return instance

    def __repr__(self) -> str:
        return f"Span(start={self.start}, end={self.end})"


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        span: tuple[int, int],
        url: str | None = None,
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        self.span = Span(*span)

    def __eq__(self, other: "TextNode") -> bool:
        return all([
            self.text == other.text,
            self.text_type.value == other.text_type.value,
            self.span == other.span,
            self.url == other.url,
        ])

    def __getitem__(self, key):
        return self.span[key]

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.span}, {self.url})"

    def __lt__(self, other: "TextNode") -> bool:
        return self.span < other.span

    def __le__(self, other: "TextNode") -> bool:
        return self.span <= other.span

    def __gt__(self, other: "TextNode") -> bool:
        return self.span > other.span

    def __ge__(self, other: "TextNode") -> bool:
        return self.span >= other.span
