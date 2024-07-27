import pathlib
import hashlib
import subprocess
import typing
import itertools
import collections
import pytest

import utils
import puzzle_generator.create_puzzle as cp
import puzzle_generator.puzzle_data_encryption as pde


_PuzzleTestCase = collections.namedtuple(
    "_PuzzleTestCase",
    [
        "puzzle",
        "all_good_answers",
        "all_good_answers_output",
        "second_answer_wrong",
        "second_answer_wrong_output",
        "first_answer_wrong",
        "first_answer_wrong_output",
    ],
)


@pytest.fixture(name="puzzle_tc")
def fixture_puzzle_tc():
    puzzle = {
        "str": "Question 1?",
        "pass": "Answer 1",
        "rest": {
            "str": "Question 2?",
            "pass": "Is this the final answer?",
            "rest": {"str": "Congratulations!"},
        },
    }
    return _PuzzleTestCase(
        puzzle=puzzle,
        all_good_answers=["Answer 1", "Is this the final answer?"],
        all_good_answers_output="Question 1?\nQuestion 2?\nCongratulations!\n",
        second_answer_wrong=["Answer 1", "This is a wrong answer"],
        second_answer_wrong_output=(
            "Question 1?\nQuestion 2?\nThis is a wrong answer. Try again!\n"
        ),
        first_answer_wrong=["This is a wrong answer"],
        first_answer_wrong_output="Question 1?\nThis is a wrong answer. Try again!\n",
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
    return subprocess.run(
        ["python3", puzzle_name],
        cwd=puzzle_dir,
        input="\n".join(answers),
        text=True,
        capture_output=True,
        check=False,
    )


_CONFIGURATIONS = [
    {},
    {"proc_hasher": hashlib.md5},
    {"proc_hasher": hashlib.sha1, "signature_hasher": hashlib.sha3_224},
    {"signature_hasher": hashlib.blake2b},
    {"encryption": "simple", "signature_hasher": hashlib.blake2b},
    {
        "encryption": "spiced",
        "proc_hasher": hashlib.sha224,
        "signature_hasher": hashlib.sha3_224,
        "proc_spices": [b"\0"],
    },
    {
        "encryption": "spiced",
        "proc_hasher": hashlib.sha3_224,
        "signature_hasher": hashlib.sha224,
        "proc_spices": [b"\1"],
        "signature_spices": [b"\2"],
    },
]


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_all_good_answers(
    puzzle_tc,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    cp.create(puzzle_tc.puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, puzzle_tc.all_good_answers)

    assert res.returncode == 0
    assert res.stdout == puzzle_tc.all_good_answers_output
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_second_answer_wrong(
    puzzle_tc,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    cp.create(puzzle_tc.puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, puzzle_tc.second_answer_wrong)
    assert res.returncode == 1
    assert res.stdout == puzzle_tc.second_answer_wrong_output
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_first_answer_wrong(
    puzzle_tc,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    cp.create(puzzle_tc.puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, puzzle_tc.first_answer_wrong)
    assert res.returncode == 1
    assert res.stdout == puzzle_tc.first_answer_wrong_output
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

_ENCRYPT_DECRYPT_PAIRS = [
    utils.get_simple_encrypt_decrypt_pair(*_)
    for _ in itertools.product(_SOME_HASHES, repeat=2)
] + [
    utils.get_spiced_simple_encrypt_decrypt_pair(*_, _PROC_SPICES, _SIGNATURE_SPICES)
    for _ in itertools.product(_SOME_HASHES, repeat=2)
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
    encrypted_puzzle = pde.encrypt_data(puzzle_tc.puzzle, encrypt)
    cp.run_puzzle(
        encrypted_puzzle, decrypt, _get_input_simulator(puzzle_tc.all_good_answers)
    )
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.all_good_answers_output


@pytest.mark.parametrize(("encrypt", "decrypt"), _ENCRYPT_DECRYPT_PAIRS)
def test_run_puzzle_second_answer_wrong(capsys, puzzle_tc, encrypt, decrypt) -> None:
    encrypted_puzzle = pde.encrypt_data(puzzle_tc.puzzle, encrypt)
    with pytest.raises(SystemExit) as exc_info:
        cp.run_puzzle(
            encrypted_puzzle,
            decrypt,
            _get_input_simulator(puzzle_tc.second_answer_wrong),
        )
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.second_answer_wrong_output
    assert exc_info.type is SystemExit
    assert exc_info.value.code == 1


@pytest.mark.parametrize(("encrypt", "decrypt"), _ENCRYPT_DECRYPT_PAIRS)
def test_run_puzzle_first_answer_wrong(capsys, puzzle_tc, encrypt, decrypt) -> None:
    encrypted_puzzle = pde.encrypt_data(puzzle_tc.puzzle, encrypt)
    with pytest.raises(SystemExit) as exc_info:
        cp.run_puzzle(
            encrypted_puzzle,
            decrypt,
            _get_input_simulator(puzzle_tc.first_answer_wrong),
        )
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.first_answer_wrong_output
    assert exc_info.type is SystemExit
    assert exc_info.value.code == 1
