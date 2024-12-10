import re

from bddssg.textnode import TextNode, TextType


def __split_node_delimter(
    old: TextNode,
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    try:
        pre, target, post = old.text.split(delimiter, maxsplit=2)
    except ValueError:
        return [old]

    out = []
    out.extend(
        __split_node_delimter(TextNode(pre, TextType.TEXT), delimiter, text_type)
    )
    out.extend(__split_node_delimter(TextNode(target, text_type), delimiter, text_type))
    out.extend(
        __split_node_delimter(TextNode(post, TextType.TEXT), delimiter, text_type)
    )

    return list(filter(lambda node: node.text, out))


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    out = []
    for old in old_nodes:
        new = __split_node_delimter(old, delimiter, text_type)
        out.extend(new)
    return out


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    PATTERN = r"(?<=!)\[(.*?)\]\((.*?)\)"
    return re.findall(PATTERN, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    PATTERN = r"(?<!!)\[(.*?)]\((.*?)\)"
    return re.findall(PATTERN, text)


def __split_node_image(old: TextNode, images: list[tuple[str, str]]) -> list[TextNode]:
    out = []
    remaining_text = old.text

    for alt, url in images:
        pattern = rf"![{alt}]({url})"

        while pattern in remaining_text:
            pre, post = remaining_text.split(pattern, 1)
            out.append(TextNode(pre, TextType.TEXT))
            out.append(TextNode(alt, TextType.IMAGE, url))

            remaining_text = post

    out.append(TextNode(remaining_text, old.text_type))
    return list(filter(lambda node: node.text, out))


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    out = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            out.append(old)
            continue

        images = extract_markdown_images(old.text)
        out.extend(__split_node_image(old, images))

    return out


def __split_node_link(old: TextNode, images: list[tuple[str, str]]) -> list[TextNode]:
    out = []
    remaining_text = old.text

    for text, url in images:
        pattern = rf"[{text}]({url})"

        while pattern in remaining_text:
            pre, post = remaining_text.split(pattern, 1)
            out.append(TextNode(pre, TextType.TEXT))
            out.append(TextNode(text, TextType.LINK, url))

            remaining_text = post

    out.append(TextNode(remaining_text, old.text_type))
    return list(filter(lambda node: node.text, out))


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    out = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            out.append(old)
            continue

        links = extract_markdown_links(old.text)
        out.extend(__split_node_link(old, links))

    return out
