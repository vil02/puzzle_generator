import hashlib
import itertools
import pytest

from .. import utils


_SOME_HASHES = [
    hashlib.md5,
    hashlib.sha512,
    hashlib.sha3_512,
    hashlib.blake2s,
]


_PROC_SPICES = [b"a", b"bb", b"ccc", b"dddd"]
_SIGNATURE_SPICES = [b"XXX", b"YY", b"Z"]


@pytest.mark.parametrize("in_bytes", utils.BYTES_LIST)
@pytest.mark.parametrize("in_pass", utils.BYTES_LIST)
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
def test_encryption_decryption(in_bytes, in_pass, encrypt, decrypt):
    encrypted = encrypt(in_bytes, in_pass)

    assert encrypted != in_bytes
    decrypted = decrypt(encrypted, in_pass)
    assert decrypted == in_bytes
    if len(in_bytes) > 1:  # there were some hash-collisions, when len(in_bytes) == 1
        assert decrypt(encrypted, in_pass + b"?") is None
