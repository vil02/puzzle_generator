import string
import hashlib
import itertools
import pytest

import puzzle_generator.simple_encryption as se
import puzzle_generator.spiced_simple_encryption as sse


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


_PROC_SPICES = [b"a", b"bb", b"ccc", b"dddd"]
_SIGNATURE_SPICES = [b"XXX", b"YY", b"Z"]


def _get_simple_encrypt_decrypt_pair(*args):
    return se.get_encrypt(*args), se.get_decrypt(*args)


def _get_spiced_simple_encrypt_decrypt_pair(*args):
    return sse.get_encrypt(*args), sse.get_decrypt(*args)


@pytest.mark.parametrize("in_str", _STRS)
@pytest.mark.parametrize("in_pass", _STRS)
@pytest.mark.parametrize(
    ("encrypt", "decrypt"),
    [
        _get_simple_encrypt_decrypt_pair(*_)
        for _ in itertools.product(_SOME_HASHES, repeat=2)
    ]
    + [
        _get_spiced_simple_encrypt_decrypt_pair(*_, _PROC_SPICES, _SIGNATURE_SPICES)
        for _ in itertools.product(_SOME_HASHES, repeat=2)
    ],
)
def test_encryption_decryption(in_str, in_pass, encrypt, decrypt):
    encrypted, reshash = encrypt(in_str, in_pass)
    if in_str:
        assert encrypted != in_str
    else:
        assert not encrypted
    decrypted = decrypt(encrypted, in_pass, reshash)
    assert decrypted == in_str
    if in_str:
        assert decrypt(encrypted, in_pass + "?", reshash) is None
