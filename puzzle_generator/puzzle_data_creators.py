import typing


def question_answer_list_to_dict(qa_list: list[str]):
    if len(qa_list) % 2 == 0:
        raise ValueError("The question/answer list must have odd length.")
    if len(qa_list) == 1:
        return {"str": qa_list[0]}
    return {
        "str": qa_list[0],
        "pass": qa_list[1],
        "rest": question_answer_list_to_dict(qa_list[2:]),
    }


def _qa_list_and_hints_from_puzzle_with_hints(
    puzzle_description: typing.Sequence[
        tuple[str, str, typing.Callable[[str], str] | None] | str
    ],
) -> tuple[list[str], list[typing.Callable[[str], str] | None]]:
    qa_list: list[str] = []
    hints: list[typing.Callable[[str], str] | None] = []
    for _ in puzzle_description[:-1]:
        question, answer, hint = _
        qa_list += [question, answer]
        hints.append(hint)
    if not isinstance(puzzle_description[-1], str):
        raise ValueError(
            "In case of puzzle with hints, "
            "the last entry of the puzzle_description must be a string"
        )
    qa_list.append(puzzle_description[-1])
    return qa_list, hints


def extract_qa_list_and_hints(
    puzzle_description: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
) -> tuple[list[str], list[typing.Callable[[str], str] | None]]:
    if isinstance(puzzle_description, list) and all(
        isinstance(_, str) for _ in puzzle_description
    ):
        qa_list: list[str] = puzzle_description
        hints: list[typing.Callable[[str], str] | None] = []
    else:
        qa_list, hints = _qa_list_and_hints_from_puzzle_with_hints(puzzle_description)
    return qa_list, hints
