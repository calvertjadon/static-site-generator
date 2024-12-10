import pytest
from bddssg.htmlnode import HTMLNode


def test_tohtml_raises() -> None:
    node = HTMLNode()
    with pytest.raises(NotImplementedError):
        node.to_html()


@pytest.mark.parametrize(
    "props,expected",
    [
        ({"href": "google.com", "style": "bold"}, 'href="google.com" style="bold"'),
        ({}, ""),
        ({"value": "asdf"}, 'value="asdf"'),
        ({"target": "_blank"}, 'target="_blank"'),
    ],
)
def test_props(props: dict[str, str], expected: str) -> None:
    node = HTMLNode(props=props)
    assert node.props_to_html() == expected
