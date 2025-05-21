import typing

from puzzle_generator.create_puzzle import create


def must_be_int(in_str: str) -> str:
    return str(int(in_str))


def make_fist_char_upper(in_str: str) -> str:
    return in_str[0].upper() + in_str[1:]


_PUZZLE: list[tuple[str, str, typing.Callable[[str], str]] | str] = [
    ("What is 1+1?", "2", must_be_int),
    ("What is my name?", "Piotr", make_fist_char_upper),
    "Congratulations, you solved this quiz!",
]

print(create(_PUZZLE))
