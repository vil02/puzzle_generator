import hashlib
import itertools
import pytest

import utils
import puzzle_generator.puzzle_data_encryption as pde

_SOME_HASHES = [
    hashlib.sha1,
    hashlib.sha256,
]


_PROC_SPICES = [b"a"]
_SIGNATURE_SPICES = [b"1", b"12"]


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
@pytest.mark.parametrize(
    ("encrypt", "decrypt"),
    [
        utils.get_simple_encrypt_decrypt_pair(*_)
        for _ in itertools.product(_SOME_HASHES, repeat=2)
    ]
    + [
        utils.get_spiced_simple_encrypt_decrypt_pair(
            *_, _PROC_SPICES, _SIGNATURE_SPICES
        )
        for _ in itertools.product(_SOME_HASHES, repeat=2)
    ],
)
def test_pde(in_puzzle, encrypt, decrypt):
    encrypted_puzzle = pde.encrypt_data(in_puzzle, encrypt)
    tmp_puzzle_data = in_puzzle
    while "rest" in encrypted_puzzle:
        cur_pass = tmp_puzzle_data["pass"]
        assert tmp_puzzle_data["str"] == encrypted_puzzle["str"]
        assert (
            pde.decrypt_data(
                encrypted_puzzle["rest"],
                cur_pass + "!",
                decrypt,
            )
            is None
        )
        encrypted_puzzle = pde.decrypt_data(
            encrypted_puzzle["rest"],
            cur_pass,
            decrypt,
        )
        tmp_puzzle_data = tmp_puzzle_data["rest"]
    assert encrypted_puzzle == tmp_puzzle_data
