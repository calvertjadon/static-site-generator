from bddssg.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent node must contain a tag")

        if not self.children:
            raise ValueError("Parent node must contain children")

        out = ""
        for child in self.children:
            out += child.to_html()

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{out}</{self.tag}>"

        return f"<{self.tag}>{out}</{self.tag}>"
