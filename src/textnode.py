class TextNode:
    def __init__(self, text: str, text_type: str, url: str):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return "TextNode(text={}, text_type={}, url={})".format(
            self.text, self.text_type, self.url
        )
