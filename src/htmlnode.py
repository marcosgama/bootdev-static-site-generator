class HTMLNode:
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
        raise NotImplementedError("Override this method")

    def props_to_html(self) -> str:
        html = []
        if self.props:
            for key, val in self.props.items():
                html.append(f' {key}="{val}"')
            return "".join(html)
        return ""
