import typing

import pytest

import puzzle_generator.hints_utils as hu


def fun_a(in_str: str) -> str:
    return in_str


def fun_b(in_str: str) -> str:
    return in_str + in_str


@pytest.mark.parametrize(
    ("hints"),
    [
        ([None]),
        ([None, None]),
        ([fun_a]),
        ([fun_a, fun_a, fun_a]),
        ([None, fun_a, fun_b, fun_b, fun_a, fun_a, fun_a, fun_b]),
    ],
)
def test_hints_utils(hints: list[typing.Callable[[str], str] | None]) -> None:
    unique_hints, hint_to_index = hu.compute_hint_to_index(hints)
    assert len(unique_hints) == len(set(hints))
    assert all(unique_hints[hint_to_index[hint]] == hint for hint in hints)
