import pytest
from bddssg.inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from bddssg.textnode import TextNode, TextType


@pytest.mark.parametrize(
    "text,delimiter,text_type,expected",
    [
        (
            "this is some **bold** text.",
            "**",
            TextType.BOLD,
            [
                TextNode("this is some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
        ),
        (
            "this is some *italic* text.",
            "*",
            TextType.ITALIC,
            [
                TextNode("this is some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        ),
        (
            "this is some _italic_ text.",
            "_",
            TextType.ITALIC,
            [
                TextNode("this is some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        ),
        (
            "*italic* text.",
            "*",
            TextType.ITALIC,
            [
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        ),
        (
            "*italic**italic*",
            "*",
            TextType.ITALIC,
            [
                TextNode("italic", TextType.ITALIC),
                TextNode("italic", TextType.ITALIC),
            ],
        ),
        (
            "**bold***italic*",
            "**",
            TextType.BOLD,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("*italic*", TextType.TEXT),
            ],
        ),
    ],
)
def test_split_delimiter(
    text: str,
    delimiter: str,
    text_type: TextType,
    expected: list[TextNode],
):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], delimiter, text_type)
    assert new_nodes == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("![my_alt_text](my_url)", [("my_alt_text", "my_url")]),
        (
            "![my_alt_text](my_url)![my alt text](my url)[my link text](my link url)",
            [("my_alt_text", "my_url"), ("my alt text", "my url")],
        ),
    ],
)
def test_extract_images(text: str, expected: list[tuple[str, str]]):
    result = extract_markdown_images(text)
    assert result == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("![my_alt_text](my_url)", []),
        ("[my_alt_text](my_url)", [("my_alt_text", "my_url")]),
        (
            "![my_alt_text](my_url)![my alt text](my url)[my link text](my link url)",
            [("my link text", "my link url")],
        ),
    ],
)
def test_extract_links(text: str, expected: list[tuple[str, str]]):
    result = extract_markdown_links(text)
    assert result == expected


def test_split_image():
    node = TextNode(
        "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_image([node])
    assert new_nodes == [
        TextNode("This is text with an image ", TextType.TEXT),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
    ]


def test_split_link():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_link([node])
    assert new_nodes == [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
    ]


def test_split_link_with_image():
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and an image ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_link([node])
    assert new_nodes == [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(
            " and an image ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        ),
    ]
