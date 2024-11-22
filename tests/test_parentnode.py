import pytest

from bddssg.htmlnode import HTMLNode
from bddssg.leafnode import LeafNode
from bddssg.parentnode import ParentNode


@pytest.mark.parametrize(
    "expected,children,props",
    [
        (
            "<parent><child1>asdf</child1></parent>",
            [
                LeafNode(tag="child1", value="asdf"),
            ],
            {},
        ),
        (
            "<parent><child1>asdf</child1><child2>1234</child2></parent>",
            [
                LeafNode(tag="child1", value="asdf"),
                LeafNode(tag="child2", value="1234"),
            ],
            {},
        ),
        (
            "<parent><parent2><child1>asdf</child1></parent2><child2>1234</child2></parent>",
            [
                ParentNode(
                    tag="parent2",
                    children=[
                        LeafNode(tag="child1", value="asdf"),
                    ],
                ),
                LeafNode(tag="child2", value="1234"),
            ],
            {},
        ),
        (
            '<parent key="value"><child>asdf</child></parent>',
            [
                LeafNode(tag="child", value="asdf"),
            ],
            {"key": "value"},
        ),
    ],
)
def test_parent(expected: str, children: list[HTMLNode], props: dict[str, str]):
    parent = ParentNode(tag="parent", children=children, props=props)
    assert expected == parent.to_html()
