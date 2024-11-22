from bddssg.htmlnode import HTMLNode
from bddssg.leafnode import LeafNode
from bddssg.textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    props = None

    match text_node.text_type:
        case TextType.TEXT:
            tag = None
            value = text_node.text
        case TextType.BOLD:
            tag = "b"
            value = text_node.text

        case TextType.ITALIC:
            tag = "i"
            value = text_node.text

        case TextType.CODE:
            tag = "code"
            value = text_node.text

        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("links must contain a url")

            tag = "a"
            value = text_node.text
            props = {"href": text_node.url}

        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("images must contain a url")

            tag = "img"
            value = ""
            props = {"src": text_node.url, "alt": text_node.text}

        case _:
            raise Exception("Invalid text type provided")

    return LeafNode(
        value=value,
        tag=tag,
        props=props,
    )
