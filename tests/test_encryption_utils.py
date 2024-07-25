import string
import hashlib
import itertools
import pytest

import puzzle_generator.simple_encryption_utils as seu


_STRS = [
    "",
    "some_STR?!",
    string.printable,
    string.whitespace,
    "ąęćśłńóżźĄĘĆŚŁŃÓŻŹ",
    "some_msg_with 🔨 and 🛷!",
    "🎮🎈🥅🐾 a🎄b",
    "🏀",
]

_SOME_HASHES = [
    hashlib.md5,
    hashlib.sha512,
    hashlib.sha3_512,
    hashlib.blake2s,
]


def _get_encrypt_decrypt_pair(proc_hasher, signature_hasher):
    return seu.get_encrypt(proc_hasher, signature_hasher), seu.get_decrypt(
        proc_hasher, signature_hasher
    )


@pytest.mark.parametrize("in_str", _STRS)
@pytest.mark.parametrize("in_pass", _STRS)
@pytest.mark.parametrize(
    ("encrypt", "decrypt"),
    [_get_encrypt_decrypt_pair(*_) for _ in itertools.product(_SOME_HASHES, repeat=2)],
)
def test_seu(in_str, in_pass, encrypt, decrypt):
    encrypted, reshash = encrypt(in_str, in_pass)
    if in_str:
        assert encrypted != in_str
    else:
        assert not encrypted
    decrypted = decrypt(encrypted, in_pass, reshash)
    assert decrypted == in_str
    if in_str:
        assert decrypt(encrypted, in_pass + "?", reshash) is None
