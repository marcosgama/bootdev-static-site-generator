from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return "LeafNode(self.value, self.tag, self.props)"

    def to_html(self):
        if self.tag is None:
            return r"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
