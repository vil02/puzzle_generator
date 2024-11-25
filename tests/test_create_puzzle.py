import pathlib
import subprocess  # nosec B404
import typing
import collections
import importlib.metadata
import black
import pytest

import puzzle_generator.create_puzzle as cp
import puzzle_generator.run_puzzle as rp
import puzzle_generator.puzzle_data_creators as pdc
import puzzle_generator.puzzle_data_encryption as pde

from . import utils

_PuzzleTestCase = collections.namedtuple(
    "_PuzzleTestCase",
    [
        "qa_list",
        "input",
        "output",
    ],
)


def _get_input(qa_list: typing.List[str]) -> typing.List[str]:
    return [_ for num, _ in enumerate(qa_list) if num % 2 == 1]


def _get_positive_output(qa_list: typing.List[str]) -> str:
    return "\n".join(_ for num, _ in enumerate(qa_list) if num % 2 == 0) + "\n"


def _positive_puzzle_tc(qa_list: typing.List[str]) -> _PuzzleTestCase:
    return _PuzzleTestCase(
        qa_list=qa_list, input=_get_input(qa_list), output=_get_positive_output(qa_list)
    )


_QA_LIST_1 = [
    "Question 1?",
    "Answer 1",
    "Question 2?",
    "Is this the final answer?",
    "Congratulations!",
]

_MULTILINE_QUESTION = (
    "Question 1❓\n"
    "-very-long-line----------------------------------------------------"
    "-------------------------------------------------------------------"
    "------------------------------------------------end-of-long-line-\n"
    "With several lines!\n"
)

_QA_LIST_2 = [
    _MULTILINE_QUESTION,
    "1",
    "Q2?",
    "A2",
    "😄",
]

_POSITIVE_PUZZLE_TCS = [
    _positive_puzzle_tc(_QA_LIST_1),
    _positive_puzzle_tc(_QA_LIST_2),
]

_NEGATIVE_PUZZLE_TCS = [
    _PuzzleTestCase(
        qa_list=_QA_LIST_1,
        input=["Answer 1", "This is a wrong answer"],
        output="Question 1?\nQuestion 2?\nThis is a wrong answer. Try again!\n",
    ),
    _PuzzleTestCase(
        qa_list=_QA_LIST_1,
        input=["This is a wrong answer"],
        output="Question 1?\nThis is a wrong answer. Try again!\n",
    ),
    _PuzzleTestCase(
        qa_list=_QA_LIST_2,
        input=["Wrong!"],
        output=_MULTILINE_QUESTION
        + """
This is a wrong answer. Try again!
""",
    ),
]


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
    assert (
        f"puzzle-generator {importlib.metadata.version('puzzle-generator')}"
        in in_puzzle
    )
    assert all(len(_) <= 88 for _ in in_puzzle.splitlines())
    with open(in_puzzle_path, "w", encoding="utf-8") as puzzle_file:
        puzzle_file.write(in_puzzle)
    return _run_puzzle_file(in_puzzle_path, answers)


_CONFIGURATIONS = [
    {},
    {"encryption": "simple"},
    {"encryption": "spiced"},
    {"scrypt_params": {"n": 2**4, "p": 2, "maxmem": 200000}},
    {"signature_params": {"digest": "sha3_384"}},
    {"encryption": "simple", "scrypt_params": {"n": 2**3, "maxmem": 100000}},
    {"encryption": "simple", "signature_params": {"digest": "blake2b"}},
    {"encryption": "simple", "signature_params": {"digest": "blake2s"}},
    {
        "encryption": "spiced",
        "proc_spices": [b"\1"],
        "signature_params": {"digest": "sha3_512"},
    },
    {
        "encryption": "spiced",
        "signature_spices": [b"\0", b"\10"],
        "signature_params": {"digest": "sha3_256"},
        "scrypt_params": {"n": 2**5, "r": 16, "salt": b"testSalt!!!"},
    },
]


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
@pytest.mark.parametrize("puzzle_tc", _POSITIVE_PUZZLE_TCS)
def test_all_good_answers(
    puzzle_tc: _PuzzleTestCase,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    puzzle: str = cp.create(puzzle_tc.qa_list, **configuration)
    res = _run_puzzle_str(puzzle, puzzle_tc.input, puzzle_path)

    assert res.returncode == 0
    assert res.stdout == puzzle_tc.output
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
@pytest.mark.parametrize("puzzle_tc", _NEGATIVE_PUZZLE_TCS)
def test_wrong_answers(
    puzzle_tc: _PuzzleTestCase,
    puzzle_path: pathlib.Path,
    configuration,
) -> None:
    puzzle: str = cp.create(puzzle_tc.qa_list, **configuration)
    res = _run_puzzle_str(puzzle, puzzle_tc.input, puzzle_path)
    assert res.returncode == 1
    assert res.stdout == puzzle_tc.output
    assert not res.stderr


def get_input_simulator(answers: typing.List[str]) -> typing.Callable[[], str]:
    cur_input = 0

    def _input_simulator() -> str:
        nonlocal cur_input
        res = answers[cur_input]
        cur_input += 1
        return res

    return _input_simulator


def _get_input_simulator(answers: typing.List[str]) -> typing.Callable[[], str]:
    cur_input = 0

    def _input_simulator() -> str:
        nonlocal cur_input
        res = answers[cur_input]
        cur_input += 1
        return res

    return _input_simulator


@pytest.mark.parametrize(("encrypt", "decrypt"), utils.ENCRYPT_DECRYPT_PAIRS)
@pytest.mark.parametrize("puzzle_tc", _POSITIVE_PUZZLE_TCS)
def test_run_puzzle_all_good_answers(
    capsys,
    puzzle_tc: _PuzzleTestCase,
    encrypt: typing.Callable[[bytes, bytes], bytes],
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None:
    encrypted_puzzle = pde.encrypt_data(
        pdc.question_answer_list_to_dict(puzzle_tc.qa_list), encrypt
    )
    rp.run_puzzle(encrypted_puzzle, decrypt, _get_input_simulator(puzzle_tc.input))
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.output


@pytest.mark.parametrize(("encrypt", "decrypt"), utils.ENCRYPT_DECRYPT_PAIRS)
@pytest.mark.parametrize("puzzle_tc", _NEGATIVE_PUZZLE_TCS)
def test_run_puzzle_wrong_answers(
    capsys, puzzle_tc: _PuzzleTestCase, encrypt, decrypt
) -> None:
    encrypted_puzzle = pde.encrypt_data(
        pdc.question_answer_list_to_dict(puzzle_tc.qa_list), encrypt
    )
    with pytest.raises(SystemExit) as exc_info:
        rp.run_puzzle(
            encrypted_puzzle,
            decrypt,
            _get_input_simulator(puzzle_tc.input),
        )
    captured = capsys.readouterr()
    assert captured.out == puzzle_tc.output
    assert exc_info.type is SystemExit
    assert exc_info.value.code == 1
