from bddssg.blocks import BlockType, block_to_block_type, markdown_to_blocks
from bddssg.htmlnode import HTMLNode
from bddssg.leafnode import LeafNode
from bddssg.textnode import TextNode, TextType
from bddssg.inline import split_nodes_delimiter, split_nodes_image, split_nodes_link
from bddssg.parentnode import ParentNode


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


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_to_children(text: str) -> list[HTMLNode]:
    children = []
    for text_node in text_to_textnodes(text):
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def _create_list_items(text: str) -> list[HTMLNode]:
    lines = []
    for line in text.split("\n"):
        _, other = line.split(" ", 1)
        lines.append(other)

    nodes = []
    for line in lines:
        child = ParentNode("li", text_to_children(line))
        nodes.append(child)
    return nodes


def markdown_to_html_node(md: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(md)

    nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                node = ParentNode("p", children)

            case BlockType.CODE:
                children = text_to_children(block.replace("```", "").strip())
                node = ParentNode("code", children)

            case BlockType.QUOTE:
                lines = list(
                    filter(
                        lambda line: line,
                        [line.strip() for line in block.replace(">", "").split("\n")],
                    )
                )
                children = text_to_children(" ".join(lines))
                node = ParentNode("blockquote", children)

            case BlockType.UNORDERED_LIST:
                node = ParentNode("ul", _create_list_items(block))

            case BlockType.ORDERED_LIST:
                node = ParentNode("ol", _create_list_items(block))

            case BlockType.HEADING:
                level, other = block.split(" ", 1)
                level = len(level)

                children = text_to_children(other)
                node = ParentNode(f"h{level}", children)

            case _:
                raise Exception("invalid block type", block_type)

        nodes.append(node)

    return ParentNode("div", nodes)
