import pytest

import puzzle_generator.string_to_code as stc


@pytest.mark.parametrize(
    ("in_str", "max_len", "quotes", "expected"),
    [
        ("some_str", 10, "'", "'some_str'"),
        (
            "01234567",
            5,
            "'",
            """'01234'
'567'""",
        ),
        (
            "0-2-4-6-8",
            5,
            "'",
            """'0-2-4'
'-6-8'""",
        ),
        (
            "0-2-4-6-8-",
            5,
            "'",
            """'0-2-4'
'-6-8-'""",
        ),
        (
            "0 2 4 6 8 ",
            5,
            "'",
            """'0 2 4'
' 6 8 '""",
        ),
    ],
)
def test_string_to_code(in_str: str, max_len: int, quotes: str, expected: str) -> None:
    assert stc.string_to_code(in_str, max_len, quotes) == expected
