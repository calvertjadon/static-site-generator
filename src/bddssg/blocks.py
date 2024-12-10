from enum import Enum


def markdown_to_blocks(text: str) -> list[str]:
    return list(
        filter(lambda block: block, [block.strip() for block in text.split("\n\n")])
    )


class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"
    HEADING = "heading"


def __is_heading(block: str) -> bool:
    try:
        level, _ = block.split(" ", 1)
        return all(
            [
                set(level) == {"#"},
                1 <= len(level) <= 6,
            ]
        )
    except ValueError:
        return False


def __is_code(block: str) -> bool:
    try:
        return all(
            [
                block[:3] == "```",
                block[-3:] == "```",
            ]
        )
    except IndexError:
        return False


def __is_quote(block: str) -> bool:
    lines = block.split("\n")
    try:
        return all([line[0] == ">" for line in lines])
    except IndexError:
        return False


def __is_unordered(block: str) -> bool:
    lines = block.split("\n")
    try:
        return all([line[0:2] in ("* ", "- ") for line in lines])
    except IndexError:
        return False


def __is_ordered(block: str) -> bool:
    lines = block.split("\n")
    try:
        return all([line[0:3] == f"{i+1}. " for i, line in enumerate(lines)])
    except IndexError:
        return False


def block_to_block_type(block: str) -> BlockType:
    if __is_heading(block):
        return BlockType.HEADING

    if __is_code(block):
        return BlockType.CODE

    if __is_quote(block):
        return BlockType.QUOTE

    if __is_unordered(block):
        return BlockType.UNORDERED_LIST

    if __is_ordered(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
