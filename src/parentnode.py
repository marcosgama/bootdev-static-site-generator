from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag if tag is not None else ValueError("Must have tag")
        self.children = children if children is not None else ValueError("Must have children")
        self.props = props

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        html = [f"<{self.tag}>", self.props_to_html()]
        for child in self.children:
            res = child.to_html()
            html.append(res)

        html.append(f"</{self.tag}>")
        return "".join(html)
