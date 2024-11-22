import pytest
from bddssg.convert import text_node_to_html_node
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
