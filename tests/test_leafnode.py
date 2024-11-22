import pytest
from bddssg.leafnode import LeafNode


def test_tohtml_requires_value():
    with pytest.raises(ValueError):
        leaf = LeafNode(None)  # type: ignore
        leaf.to_html()


@pytest.mark.parametrize(
    "value,tag,props,expected",
    [
        (
            "asdf",
            "a",
            {"href": "https://google.com"},
            '<a href="https://google.com">asdf</a>',
        ),
        (
            "asdf",
            "p",
            None,
            "<p>asdf</p>",
        ),
        ("asdf", None, None, "asdf"),
    ],
)
def test_tohtml_with_tag(value: str, tag: str, props: dict[str, str], expected: str):
    leaf = LeafNode(value=value, tag=tag, props=props)
    assert leaf.to_html() == expected
