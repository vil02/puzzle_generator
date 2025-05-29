import typing

import pytest

import puzzle_generator.puzzle_data_creators as pdc


@pytest.mark.parametrize(
    ("qa_list", "expected"),
    [
        (["Congratulations!"], {"str": "Congratulations!"}),
        (
            ["Question 1?", "Answer 1", "Congratulations!"],
            {
                "str": "Question 1?",
                "pass": "Answer 1",
                "rest": {"str": "Congratulations!"},
            },
        ),
        (
            [
                "What is 1+1?",
                "2",
                "What is 2+2?",
                "4",
                "What is 3+3?",
                "6",
                "Congratulations!",
            ],
            {
                "str": "What is 1+1?",
                "pass": "2",
                "rest": {
                    "str": "What is 2+2?",
                    "pass": "4",
                    "rest": {
                        "str": "What is 3+3?",
                        "pass": "6",
                        "rest": {"str": "Congratulations!"},
                    },
                },
            },
        ),
    ],
)
def test_question_answer_list_to_dict(qa_list: list[str], expected) -> None:
    assert pdc.question_answer_list_to_dict(qa_list) == expected


@pytest.mark.parametrize(
    "wrong_qa_list",
    [
        [],
        ["Question", "Answer"],
        ["Question 1", "Answer 1", "Question 2", "Answer 2"],
    ],
)
def test_question_answer_list_to_dict_raises_when_input_list_has_even_length(
    wrong_qa_list: list[str],
) -> None:
    with pytest.raises(
        ValueError, match="The question/answer list must have odd length."
    ):
        pdc.question_answer_list_to_dict(wrong_qa_list)


def _some_hint_fun_0(in_str: str) -> str:
    return in_str + in_str


def _some_hint_fun_1(in_str: str) -> str:
    return in_str + "?"


@pytest.mark.parametrize(
    ("puzzle_description", "expected"),
    [
        (["Q1", "A1", "Q2", "A3", "Final"], (["Q1", "A1", "Q2", "A3", "Final"], [])),
        (
            [
                ("Q1", "A1", _some_hint_fun_0),
                ("Q2", "A2", _some_hint_fun_1),
                ("Q3", "A3", None),
                "end!",
            ],
            (
                ["Q1", "A1", "Q2", "A2", "Q3", "A3", "end!"],
                [_some_hint_fun_0, _some_hint_fun_1, None],
            ),
        ),
    ],
)
def test_extract_qa_list_and_hints(puzzle_description, expected) -> None:
    assert pdc.extract_qa_list_and_hints(puzzle_description) == expected


def test_extract_qa_list_and_hints_raises_for_wrong_input() -> None:
    puzzle_description = [("Q1", "A1", None), ("Q2", "A2", None)]
    with pytest.raises(
        ValueError,
        match="In case of puzzle with hints, "
        "the last entry of the puzzle_description must be a string",
    ):
        pdc.extract_qa_list_and_hints(puzzle_description)


def test_extract_qa_list_and_hints_raises_for_other_wrong_input() -> None:
    puzzle_description: typing.Sequence[
        tuple[str, str, typing.Callable[[str], str] | None] | str
    ] = ["Q1", ("Q2", "A2", None), "Final"]
    with pytest.raises(
        ValueError,
        match="In case of puzzle with hints, "
        "all entires besides the last one "
        "have to be of the type "
        "tuple[str, str, typing.Callable[[str], str] | None]",
    ):
        pdc.extract_qa_list_and_hints(puzzle_description)
