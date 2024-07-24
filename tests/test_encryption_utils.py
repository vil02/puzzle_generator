import string
import pytest

import puzzle_generator.simple_encryption_utils as seu


_STRS = [
    "",
    "some_str",
    "other_strstr!?#",
    string.printable,
    string.ascii_uppercase,
    string.whitespace,
    "ąęćśłńóżźĄĘĆŚŁŃÓŻŹ",
    "some_msg_with 🔨 and 🛷!",
    "a🎄b",
    "🎮🎈🥅🐾",
    "🏀",
]


@pytest.mark.parametrize("in_str", _STRS)
@pytest.mark.parametrize("in_pass", _STRS)
@pytest.mark.parametrize(
    ("in_encrypt_str", "in_decrypt_str"), [(seu.encrypt_str, seu.decrypt_str)]
)
def test_seu(in_str, in_pass, in_encrypt_str, in_decrypt_str):
    encrypted, reshash = in_encrypt_str(in_str, in_pass)
    if in_str:
        assert encrypted != in_str
    else:
        assert not encrypted
    decrypted = in_decrypt_str(encrypted, in_pass, reshash)
    assert decrypted == in_str
    if in_str:
        assert in_decrypt_str(encrypted, in_pass + "?", reshash) is None
