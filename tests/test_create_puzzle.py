import pathlib
import hashlib
import subprocess  # nosec B404
import typing
import itertools
import collections
import black
import pytest

import puzzle_generator.create_puzzle as cp
import puzzle_generator.run_puzzle as rp
import puzzle_generator.puzzle_data_encryption as pde

from . import utils

_InputOutput = collections.namedtuple("_InputOutput", ["input", "output"])

_PuzzleTestCase = collections.namedtuple(
    "_PuzzleTestCase",
    [
        "qa_list",
        "correct",
        "wrong",
    ],
)


@pytest.fixture(name="puzzle_tc")
def fixture_puzzle_tc():
    qa_list = [
        "Question 1?",
        "Answer 1",
        "Question 2?",
        "Is this the final answer?",
        "Congratulations!",
    ]
    return _PuzzleTestCase(
        qa_list=qa_list,
        correct=_InputOutput(
            input=["Answer 1", "Is this the final answer?"],
            output="Question 1?\nQuestion 2?\nCongratulations!\n",
        ),
        wrong=[
            _InputOutput(
                input=["Answer 1", "This is a wrong answer"],
                output="Question 1?\nQuestion 2?\nThis is a wrong answer. Try again!\n",
            ),
            _InputOutput(
                input=["This is a wrong answer"],
                output="Question 1?\nThis is a wrong answer. Try again!\n",
            ),
        ],
    )


@pytest.fixture(name="puzzle_path")
def fixture_puzzle_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "puzzle.py"


def _run_puzzle_file(
    in_puzzle_path: pathlib.Path, answers: list[str]
) -> subprocess.CompletedProcess[str]:
    assert in_puzzle_path.is_file()
    puzzle_dir = in_puzzle_path.parent
    puzzle_name = in_puzzle_path.name
    return subprocess.run(  # nosec B603, B607
        ["python3", puzzle_name],
        cwd=puzzle_dir,
        input="\n".join(answers),
        text=True,
        capture_output=True,
        check=False,
    )


def _run_puzzle_str(
    in_puzzle: str, answers: list[str], in_puzzle_path: pathlib.Path
) -> subprocess.CompletedProcess[str]:
    assert in_puzzle == black.format_str(in_puzzle, mode=black.FileMode())
    with open(in_puzzle_path, "w", encoding="utf-8") as puzzle_file:
        puzzle_file.write(in_puzzle)
    return _run_puzzle_file(in_puzzle_path, answers)


_CONFIGURATIONS = [
    {},
    {"signature_hasher": hashlib.sha3_224, "n": 2**2},
    {"signature_hasher": hashlib.blake2b, "salt": b"very_bad_salt"},
    {"encryption": "simple", "signature_hasher": hashlib.blake2b},
    {
        "encryption": "spiced",
        "signature_hasher": hashlib.sha3_224,
        "proc_spices": [b"\0"],
        "n": 2**3,
        "maxmem": 0,
    },
    {
        "encryption": "spiced",
        "signature_hasher": hashlib.sha224,
        "proc_spices": [b"\1"],
        "signature_spices": [b"\2"],
        "salt": b"even_worse_salt!",
        "r": 16,
    },
]


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_all_good_answers(
    puzzle_tc,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    puzzle: str = cp.create(puzzle_tc.qa_list, **configuration)
    res = _run_puzzle_str(puzzle, puzzle_tc.correct.input, puzzle_path)

    assert res.returncode == 0
    assert res.stdout == puzzle_tc.correct.output
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_wrong_answers(
    puzzle_tc,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    for cur_wrong in puzzle_tc.wrong:
        puzzle: str = cp.create(puzzle_tc.qa_list, **configuration)
        res = _run_puzzle_str(puzzle, cur_wrong.input, puzzle_path)
        assert res.returncode == 1
        assert res.stdout == cur_wrong.output
        assert not res.stderr


def get_input_simulator(answers: typing.List[str]) -> typing.Callable[[], str]:
    cur_input = 0

    def _input_simulator() -> str:
        nonlocal cur_input
        res = answers[cur_input]
        cur_input += 1
        return res

    return _input_simulator


_SOME_HASHES = [
    hashlib.sha3_384,
    hashlib.sha3_256,
]

_PROC_SPICES = [b"11", b"22"]
_SIGNATURE_SPICES = [b"27", b"07", b"2024"]

_SOME_SCRYPT_PARAMS = [
    {"salt": b"salt_1", "n": 8, "r": 5, "p": 1},
    {"salt": b"salt_two", "n": 4, "r": 2, "p": 1},
]

_ENCRYPT_DECRYPT_PAIRS = [
    utils.get_simple_encrypt_decrypt_pair(hash, scrypt_params)
    for hash, scrypt_params in itertools.product(_SOME_HASHES, _SOME_SCRYPT_PARAMS)
] + [
    utils.get_spiced_simple_encrypt_decrypt_pair(
        hash, _PROC_SPICES, _SIGNATURE_SPICES, scrypt_params
    )
    for hash, scrypt_params in itertools.product(_SOME_HASHES, _SOME_SCRYPT_PARAMS)
]


def _get_input_simulator(answers: typing.List[str]) -> typing.Callable[[], str]:
    cur_input = 0

    def _input_simulator() -> str:
        nonlocal cur_input
        res = answers[cur_input]
        cur_input += 1
        return res

    return _input_simulator


@pytest.mark.parametrize(("encrypt", "decrypt"), _ENCRYPT_DECRYPT_PAIRS)
def test_run_puzzle_all_good_answers(capsys, puzzle_tc, encrypt, decrypt) -> None:
    encrypted_puzzle = pde.encrypt_data(
        cp.question_answer_list_to_dict(puzzle_tc.qa_list), encrypt
    )
    rp.run_puzzle(
        encrypted_puzzle, decrypt, _get_input_simulator(puzzle_tc.correct.input)
    )
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.correct.output


@pytest.mark.parametrize(("encrypt", "decrypt"), _ENCRYPT_DECRYPT_PAIRS)
def test_run_puzzle_wrong_answers(capsys, puzzle_tc, encrypt, decrypt) -> None:
    for cur_wrong in puzzle_tc.wrong:
        encrypted_puzzle = pde.encrypt_data(
            cp.question_answer_list_to_dict(puzzle_tc.qa_list), encrypt
        )
        with pytest.raises(SystemExit) as exc_info:
            rp.run_puzzle(
                encrypted_puzzle,
                decrypt,
                _get_input_simulator(cur_wrong.input),
            )
        captured = capsys.readouterr()
        assert captured.out == cur_wrong.output
        assert exc_info.type is SystemExit
        assert exc_info.value.code == 1


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
def test_question_answer_list_to_dict(qa_list, expected):
    assert cp.question_answer_list_to_dict(qa_list) == expected


@pytest.mark.parametrize(
    "wrong_qa_list",
    [
        [],
        ["Question", "Answer"],
        ["Question 1", "Answer 1", "Question 2", "Answer 2"],
    ],
)
def test_question_answer_list_to_dict_raises_when_input_list_has_even_length(
    wrong_qa_list,
):
    with pytest.raises(
        ValueError, match="The question/answer list must have odd length."
    ):
        cp.question_answer_list_to_dict(wrong_qa_list)
