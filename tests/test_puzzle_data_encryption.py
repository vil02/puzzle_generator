import typing

import pytest

import puzzle_generator.puzzle_data_encryption as pde

from . import utils


def _decrypt_data(
    puzzle_bytes: bytes,
    cur_pass: str,
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> tuple[str, bytes]:
    res = pde.decrypt_data(
        puzzle_bytes,
        cur_pass,
        decrypt,
    )
    assert res is not None
    return res


@pytest.mark.parametrize(
    "in_puzzle",
    [
        {
            "str": "This quiz has one question!",
            "pass": "Only one?",
            "rest": {
                "str": "Yes! You are the best!",
            },
        },
        {
            "str": "",
            "pass": "Empty question?",
            "rest": {
                "str": "Yes!",
            },
        },
        {
            "str": "Empty answer?",
            "pass": "",
            "rest": {
                "str": "You are right!",
            },
        },
        {
            "str": "Now the final message will be empty.",
            "pass": "😟",
            "rest": {
                "str": "",
            },
        },
        {
            "str": "Question 1",
            "pass": "Answer 1",
            "rest": {
                "str": "Question 2🐰",
                "pass": "Answer 2👍",
                "rest": {"str": "Congratulations!🎉"},
            },
        },
    ],
)
@pytest.mark.parametrize(("encrypt", "decrypt"), utils.ENCRYPT_DECRYPT_PAIRS)
def test_pde(
    in_puzzle,
    encrypt: typing.Callable[[bytes, bytes], bytes],
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None:
    encrypted_puzzle = pde.encrypt_data(in_puzzle, encrypt)
    tmp_puzzle_data = in_puzzle
    while len(encrypted_puzzle[1]) > 0:
        cur_pass = tmp_puzzle_data["pass"]
        assert tmp_puzzle_data["str"] == encrypted_puzzle[0]
        assert (
            pde.decrypt_data(
                encrypted_puzzle[1],
                cur_pass + "!",
                decrypt,
            )
            is None
        )
        encrypted_puzzle = _decrypt_data(
            encrypted_puzzle[1],
            cur_pass,
            decrypt,
        )
        tmp_puzzle_data = tmp_puzzle_data["rest"]
    assert encrypted_puzzle[0] == tmp_puzzle_data["str"]


def _decrypt_data_with_hints(
    puzzle_bytes: bytes,
    cur_pass: str,
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> tuple[str, int, bytes]:
    res = pde.decrypt_data_with_hints(
        puzzle_bytes,
        cur_pass,
        decrypt,
    )
    assert res is not None
    return res


def _assert_that_it_is_not_possible_to_decrypt_with_wrong_password(
    encrypted: bytes,
    some_wrong_password: str,
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None:
    assert pde.decrypt_data_with_hints(encrypted, some_wrong_password, decrypt) is None


@pytest.mark.parametrize(
    "in_puzzle",
    [
        {
            "str": "Q1",
            "index": 18,
            "pass": "A1",
            "rest": {
                "str": "Final_str",
            },
        },
        {
            "str": "Question 1",
            "index": 93,
            "pass": "Answer 1",
            "rest": {
                "str": "Question2💩",
                "pass": "Answer2🤠",
                "index": 771771,
                "rest": {"str": "Yeah!💥💯😻🍔🍪"},
            },
        },
        {
            "str": "Q_1",
            "index": 213,
            "pass": "A_1",
            "rest": {
                "str": "Q__3",
                "pass": "A__3",
                "index": 959595,
                "rest": {
                    "str": "Q___4",
                    "pass": "A___4",
                    "index": 39393,
                    "rest": {"str": "F1"},
                },
            },
        },
    ],
)
@pytest.mark.parametrize(("encrypt", "decrypt"), utils.ENCRYPT_DECRYPT_PAIRS)
def test_pde_with_hints(
    in_puzzle,
    encrypt: typing.Callable[[bytes, bytes], bytes],
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None:
    encrypted_puzzle = pde.encrypt_data_with_hints(in_puzzle, encrypt)
    tmp_puzzle_data = in_puzzle

    while len(encrypted_puzzle[2]) > 0:
        assert tmp_puzzle_data["str"] == encrypted_puzzle[0]
        assert tmp_puzzle_data["index"] == encrypted_puzzle[1]

        _assert_that_it_is_not_possible_to_decrypt_with_wrong_password(
            encrypted_puzzle[2], tmp_puzzle_data["pass"] + "!", decrypt
        )
        encrypted_puzzle = _decrypt_data_with_hints(
            encrypted_puzzle[2],
            tmp_puzzle_data["pass"],
            decrypt,
        )
        tmp_puzzle_data = tmp_puzzle_data["rest"]
    assert encrypted_puzzle[0] == tmp_puzzle_data["str"]
