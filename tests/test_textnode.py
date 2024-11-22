import pytest

from bddssg.textnode import TextNode, TextType


@pytest.mark.parametrize(
    "node1,node2,expected",
    [
        (
            TextNode("This is a text node", TextType.BOLD),
            TextNode("This is a text node", TextType.BOLD),
            True,
        ),
        (
            TextNode("This is a text node", TextType.BOLD),
            TextNode("This is a different text node", TextType.BOLD),
            False,
        ),
        (
            TextNode("This is a text node", TextType.BOLD),
            TextNode("This is a text node", TextType.TEXT),
            False,
        ),
        (
            TextNode("This is a text node", TextType.BOLD, "https://google.com"),
            TextNode("This is a text node", TextType.BOLD, "https://google.com"),
            True,
        ),
        (
            TextNode("This is a text node", TextType.BOLD, "https://google.com"),
            TextNode("This is a text node", TextType.BOLD),
            False,
        ),
    ],
)
def test_eq(node1: TextNode, node2: TextNode, expected: bool):
    assert (node1 == node2) is expected
