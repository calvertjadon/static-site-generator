import pytest
from bddssg.convert import (
    markdown_to_html_node,
    text_node_to_html_node,
    text_to_textnodes,
)
from bddssg.htmlnode import HTMLNode
from bddssg.parentnode import ParentNode
from bddssg.textnode import TextNode, TextType


def test_convert_text():
    node = TextNode("asdf", TextType.TEXT)
    result = text_node_to_html_node(node)
    assert result.value == node.text
    assert result.tag is None
    assert result.props is None


def test_convert_bold():
    node = TextNode("asdf", TextType.BOLD)
    result = text_node_to_html_node(node)
    assert result.value == node.text
    assert result.tag == "b"
    assert result.props is None


def test_convert_italic():
    node = TextNode("asdf", TextType.ITALIC)
    result = text_node_to_html_node(node)
    assert result.value == node.text
    assert result.tag == "i"
    assert result.props is None


def test_convert_code():
    node = TextNode("asdf", TextType.CODE)
    result = text_node_to_html_node(node)
    assert result.value == node.text
    assert result.tag == "code"
    assert result.props is None


def test_convert_link():
    node = TextNode("asdf", TextType.LINK, url="mywebsite")
    result = text_node_to_html_node(node)
    assert result.value == node.text
    assert result.tag == "a"
    assert result.props == {"href": node.url}


def test_convert_image():
    node = TextNode("asdf", TextType.IMAGE, url="myimage")
    result = text_node_to_html_node(node)
    assert result.value == ""
    assert result.tag == "img"
    assert result.props == {"src": node.url, "alt": node.text}


def test_link_requires_url():
    node = TextNode("asdf", TextType.LINK, url=None)
    with pytest.raises(ValueError):
        text_node_to_html_node(node)


def test_image_requires_url():
    node = TextNode("asdf", TextType.IMAGE, url=None)
    with pytest.raises(ValueError):
        text_node_to_html_node(node)


def test_text_to_nodes():
    result = text_to_textnodes(
        "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    )
    assert result == [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]


def test_markdown_to_html_node_paragraph():
    md = "this is paragraph text"
    result = markdown_to_html_node(md)
    assert result.to_html() == "<div><p>this is paragraph text</p></div>"


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            """
```
this is code
```
""",
            "<div><code>this is code</code></div>",
        ),
        (
            """```this is code```""",
            "<div><code>this is code</code></div>",
        ),
    ],
)
def test_markdown_to_html_node_code(text: str, expected: str):
    result = markdown_to_html_node(text)
    assert result.to_html() == expected


def test_markdown_to_html_node_quote():
    md = """
> this is
> a
> quote
    """
    result = markdown_to_html_node(md)
    assert result.to_html() == "<div><blockquote>this is a quote</blockquote></div>"


def test_markdown_to_html_node_unordered():
    md = """
- first
- second
- third
"""
    result = markdown_to_html_node(md)
    assert (
        result.to_html()
        == "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>"
    )


@pytest.mark.parametrize(
    "md,expected_node",
    [
        ("# heading 1", "<h1>heading 1</h1>"),
        ("## heading 2", "<h2>heading 2</h2>"),
        ("### heading 3", "<h3>heading 3</h3>"),
        ("#### heading 4", "<h4>heading 4</h4>"),
        ("##### heading 5", "<h5>heading 5</h5>"),
        ("###### heading 6", "<h6>heading 6</h6>"),
    ],
)
def test_markdown_to_html_node_heading(md: str, expected_node: str):
    result = markdown_to_html_node(md)
    assert result.to_html() == f"<div>{expected_node}</div>"


def test_markdown_to_html_node():
    md = """
# heading 1

> this is
> a **bold** quote

- first
- second

1. third
2. fourth with `code`
"""

    result = markdown_to_html_node(md)
    assert (
        result.to_html()
        == "<div>\
<h1>heading 1</h1>\
<blockquote>this is a <b>bold</b> quote</blockquote>\
<ul><li>first</li><li>second</li></ul>\
<ol><li>third</li><li>fourth with <code>code</code></li></ol>\
</div>"
    )
