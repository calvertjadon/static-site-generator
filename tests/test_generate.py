import pytest

from bddssg.generate import extract_title


@pytest.mark.parametrize(
    "md,expected",
    [
        ("# title", "title"),
        (
            """


#         title                       

## other heading

other stuff
""",
            "title",
        ),
    ],
)
def test_extract_title(md: str, expected: str):
    result = extract_title(md)
    assert result == expected
