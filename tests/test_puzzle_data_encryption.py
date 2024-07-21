import pytest

import puzzle_generator.puzzle_data_encryption as pde
import puzzle_generator.simple_encryption_utils as seu


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
def test_pde(in_puzzle):
    encrypted_puzzle = pde.encrypt_data(in_puzzle, seu.encrypt_str)
    tmp_puzzle_data = in_puzzle
    while "rest" in encrypted_puzzle:
        cur_pass = tmp_puzzle_data["pass"]
        assert tmp_puzzle_data["str"] == encrypted_puzzle["str"]
        assert (
            pde.decrypt_data(
                encrypted_puzzle["rest"],
                encrypted_puzzle["hash"],
                cur_pass + "!",
                seu.decrypt_str,
            )
            is None
        )
        encrypted_puzzle = pde.decrypt_data(
            encrypted_puzzle["rest"],
            encrypted_puzzle["hash"],
            cur_pass,
            seu.decrypt_str,
        )
        tmp_puzzle_data = tmp_puzzle_data["rest"]
    assert encrypted_puzzle == tmp_puzzle_data
