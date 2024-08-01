import hashlib
import itertools
import pytest

import puzzle_generator.puzzle_data_encryption as pde
from . import utils

_SOME_HASHES = [
    hashlib.sha1,
    hashlib.sha256,
]


_PROC_SPICES = [b"a"]
_SIGNATURE_SPICES = [b"1", b"12"]


_SOME_SCRYPT_PARAMS = [
    {"salt": b"some_bad_salt_0", "n": 8, "r": 5, "p": 1},
    {"salt": b"some_other_bad_salt_1", "n": 4, "r": 2, "p": 1},
]


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
        utils.get_simple_encrypt_decrypt_pair(hash, scrypt_params)
        for hash, scrypt_params in itertools.product(_SOME_HASHES, _SOME_SCRYPT_PARAMS)
    ]
    + [
        utils.get_spiced_simple_encrypt_decrypt_pair(
            hash, _PROC_SPICES, _SIGNATURE_SPICES, scrypt_params
        )
        for hash, scrypt_params in itertools.product(_SOME_HASHES, _SOME_SCRYPT_PARAMS)
    ],
)
def test_pde(in_puzzle, encrypt, decrypt):
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
        encrypted_puzzle = pde.decrypt_data(
            encrypted_puzzle[1],
            cur_pass,
            decrypt,
        )
        tmp_puzzle_data = tmp_puzzle_data["rest"]
    assert encrypted_puzzle[0] == tmp_puzzle_data["str"]
