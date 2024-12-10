import pytest
from bddssg.blocks import BlockType, block_to_block_type, markdown_to_blocks


def test_md_to_blk():
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item




"""
    result = markdown_to_blocks(text)
    assert result == [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        """* This is the first list item in a list block
* This is a list item
* This is another list item""",
    ]


@pytest.mark.parametrize(
    "block,expected",
    [
        ("# this is a heading", BlockType.HEADING),
        ("## this is a heading", BlockType.HEADING),
        ("### this is a heading", BlockType.HEADING),
        ("#### this is a heading", BlockType.HEADING),
        ("##### this is a heading", BlockType.HEADING),
        ("###### this is a heading", BlockType.HEADING),
        ("####### this is a paragraph", BlockType.PARAGRAPH),
    ],
)
def test_blk_to_blktype_heading(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected


@pytest.mark.parametrize(
    "block,expected",
    [("```\nthis is a code block\n```", BlockType.CODE)],
)
def test_blk_to_blktype_code(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected


@pytest.mark.parametrize(
    "block,expected",
    [(">this is a\n>quote block", BlockType.QUOTE)],
)
def test_blk_to_blktype_quote(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected


@pytest.mark.parametrize(
    "block,expected",
    [
        ("* this\n* is\n* a\n* list", BlockType.UNORDERED_LIST),
        ("- this\n- is\n- a\n- list", BlockType.UNORDERED_LIST),
        ("*so is this", BlockType.PARAGRAPH),
        ("-and this", BlockType.PARAGRAPH),
    ],
)
def test_blk_to_blktype_unordered(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected


@pytest.mark.parametrize(
    "block,expected",
    [
        ("1. first\n2. second\n3. third", BlockType.ORDERED_LIST),
        ("1.this is\n2.also a paragraph", BlockType.PARAGRAPH),
        ("1. and so\n1. is this", BlockType.PARAGRAPH),
    ],
)
def test_blk_to_blktype_ordered(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected


@pytest.mark.parametrize(
    "block,expected",
    [
        ("this is a paragraph", BlockType.PARAGRAPH),
    ],
)
def test_blk_to_blktype_paragraph(block: str, expected: str):
    result = block_to_block_type(block)
    assert result == expected
