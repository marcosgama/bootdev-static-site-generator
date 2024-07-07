class HtmlNode:
    def __init__(
        self, tag: str, value: str | None, children: list | None, props: dict | None
    ) -> None:
        self.tag = tag if tag else None
        self.value = value if value else None
        self.children = children if children else []
        self.props = props if props else {}

    def __repr__(self) -> str:
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("Child classes must implement this method")

    def props_to_html(self) -> str:
        props = ""
        for key, value in self.props.items():
            props += f' {key}="{value}"'
        return props.strip()


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict | None) -> None:
        super().__init__(tag, value, None, props)

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

    def to_html(self) -> str:
        match self:
            case LeafNode(tag=tag, value=value, props=props) if not tag:
                return rf"{value}"
            case LeafNode(tag=tag, value=value, props=props) if not value:
                raise ValueError("Leaf node must have a value")
            case LeafNode(tag=tag, value=value, props=props) if not props:
                return f"<{tag}>{value}</{tag}>"
            case LeafNode(tag=tag, value=value, props=props):
                return f"<{tag} {self.props_to_html()}>{value}</{tag}>"


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict | None) -> None:
        if not tag:
            raise ValueError("Parent node must have a tag")
        if not children or len(children) == 0:
            raise ValueError("Parent node must have children")

        super().__init__(tag, None, children, props)

    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag}, children={
            self.children}, props={self.props})"

    def to_html(self) -> str:
        match self:
            case ParentNode(tag=tag, children=children, props=props) if not tag:
                raise ValueError("Parent node must have a tag")
            case ParentNode(tag=tag, children=children, props=props) if not children:
                raise ValueError("Parent node must have children")
            case ParentNode(tag=tag, children=children, props=props):
                html = f"<{tag}>CHILDREN_HTML</{tag}>"
                if props:
                    html = f"<{tag} {
                        self.props_to_html()}>CHILDREN_HTML</{tag}>"
                children_html = ""
                for child in self.children:
                    children_html += child.to_html()
                return html.replace("CHILDREN_HTML", children_html)
