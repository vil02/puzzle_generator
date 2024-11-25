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
