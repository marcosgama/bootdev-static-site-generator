class HTMLNode:
    """
    Base class for creating intermediate representations of Markdown to HTML.
    It is a node in the HTML tree.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> None:
        """
        Converts text to HTML representation
        """
        raise NotImplementedError("Override this method")

    def props_to_html(self) -> str:
        """
        Converts the properties dictionary into a string.

        Returns: str
        """
        html = []
        if self.props:
            for key, val in self.props.items():
                html.append(f' {key}="{val}"')
            return "".join(html)
        return ""


class ParentNode(HTMLNode):
    """
    Represents a node with children in the HTML tree
    """

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag if tag is not None else ValueError("Must have tag")
        self.children = children if children is not None else ValueError(
            "Must have children")
        self.props = props

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self) -> str:
        """
        Handles the nesting of HTML children nodes inside of one another

        Returns: str
        """
        html = [f"<{self.tag}>", self.props_to_html()]
        for child in self.children:
            res = child.to_html()
            html.append(res)

        html.append(f"</{self.tag}>")
        return "".join(html)


class LeafNode(HTMLNode):
    """
    Represents a node without children in the HTML tree
    """

    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other: "LeafNode"):
        return all([self.tag == other.tag, self.value == other.value, self.props == other.props])

    def to_html(self) -> str:
        """
        Converts text to HTML representation
        """
        if self.tag is None:
            return rf"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
