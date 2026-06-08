import typing

from . import hints_utils as hu
from . import randomise_index as ri


def _is_str_list(
    in_list: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
) -> typing.TypeGuard[list[str]]:
    return isinstance(in_list, list) and all(isinstance(_, str) for _ in in_list)


def is_sq_list_element(
    in_element: tuple[str, str, typing.Callable[[str], str] | None] | str,
) -> typing.TypeGuard[tuple[str, str, typing.Callable[[str], str] | None]]:
    if isinstance(in_element, str):
        return False
    question, answer, hint = in_element
    return (
        isinstance(question, str)
        and isinstance(answer, str)
        and (callable(hint) or hint is None)
    )


def _is_sq_list(
    in_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str],
) -> typing.TypeGuard[
    typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]]
]:
    return isinstance(in_list, list) and all(is_sq_list_element(_) for _ in in_list)


def _q_list_to_sq_list(
    q_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str],
) -> tuple[typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]], str]:
    final_str = q_list[-1]
    assert isinstance(final_str, str)
    sq_list = q_list[:-1]
    assert _is_sq_list(sq_list)
    return sq_list, final_str


def _puzzle_description_to_q_list(
    puzzle_description: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
) -> typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]:
    if _is_str_list(puzzle_description):
        return qa_list_to_q_list(puzzle_description)
    return puzzle_description


def puzzle_description_to_sq_list(
    puzzle_description: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
) -> tuple[typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]], str]:
    return _q_list_to_sq_list(_puzzle_description_to_q_list(puzzle_description))


def qa_list_to_q_list(
    qa_list: list[str],
) -> list[tuple[str, str, typing.Callable[[str], str] | None] | str]:
    if len(qa_list) % 2 == 0:
        raise ValueError("The question/answer list must have odd length.")
    if len(qa_list) == 1:
        return [qa_list[0]]

    return [(qa_list[0], qa_list[1], None)] + qa_list_to_q_list(qa_list[2:])


def extract_hints(
    sq_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]],
) -> list[typing.Callable[[str], str] | None]:
    return [_[2] for _ in sq_list]


def hints_info(
    sq_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]],
) -> tuple[
    list[typing.Callable[[str], str] | None] | None,
    dict[typing.Callable[[str], str] | None, int] | None,
]:
    hints = extract_hints(sq_list)
    unique_hints, hint_to_index = (
        hu.compute_hint_to_index(hints)
        if any(_ is not None for _ in hints)
        else (None, None)
    )
    return unique_hints, hint_to_index


def sq_list_to_dict(
    sq_list: typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None]],
    final_str: str,
    hint_to_index: dict[typing.Callable[[str], str] | None, int] | None = None,
):
    if not sq_list:
        return {"str": final_str}
    res = {
        "str": sq_list[0][0],
        "pass": sq_list[0][1],
        "rest": sq_list_to_dict(sq_list[1:], final_str, hint_to_index),
    }
    if hint_to_index is not None:
        res["index"] = ri.randomise_index(
            hint_to_index[sq_list[0][2]], len(hint_to_index)
        )
    return res
