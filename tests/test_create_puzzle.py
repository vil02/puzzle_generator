import pathlib
import hashlib
import subprocess
import pytest

import puzzle_generator.create_puzzle as cp


@pytest.fixture(name="puzzle")
def fixture_puzzle():
    return {
        "str": "Question 1?",
        "pass": "Answer 1",
        "rest": {
            "str": "Question 2?",
            "pass": "Is this the final answer?",
            "rest": {"str": "Congratulations!"},
        },
    }


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
]


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_all_good_answers(puzzle, puzzle_path: pathlib.Path, configuration) -> None:
    cp.create(puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, ["Answer 1", "Is this the final answer?"])

    assert res.returncode == 0
    assert res.stdout == "Question 1?\nQuestion 2?\nCongratulations!\n"
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_second_answer_wrong(puzzle, puzzle_path: pathlib.Path, configuration) -> None:
    cp.create(puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, ["Answer 1", "This is a wrong answer"])
    assert res.returncode == 1
    assert (
        res.stdout == "Question 1?\nQuestion 2?\nThis is a wrong answer. Try again!\n"
    )
    assert not res.stderr


@pytest.mark.parametrize("configuration", _CONFIGURATIONS)
def test_first_answer_wrong(puzzle, puzzle_path: pathlib.Path, configuration) -> None:
    cp.create(puzzle, puzzle_path, **configuration)
    res = _run_puzzle_file(puzzle_path, ["This is a wrong answer."])
    assert res.returncode == 1
    assert res.stdout == "Question 1?\nThis is a wrong answer. Try again!\n"
    assert not res.stderr
