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

_SOME_SCRYPT_PARAMS = [
    {"salt": b"some_bad_salt", "n": 8, "r": 10, "p": 1},
    {"salt": b"some_other_bad_salt", "n": 16, "r": 20, "p": 1},
]

_PROC_SPICES = [b"a", b"bb", b"ccc", b"dddd"]
_SIGNATURE_SPICES = [b"XXX", b"YY", b"Z"]


@pytest.mark.parametrize("in_bytes", utils.BYTES_LIST)
@pytest.mark.parametrize("in_pass", utils.BYTES_LIST)
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
def test_encryption_decryption(in_bytes, in_pass, encrypt, decrypt):
    encrypted = encrypt(in_bytes, in_pass)

    assert encrypted != in_bytes
    decrypted = decrypt(encrypted, in_pass)
    assert decrypted == in_bytes
    if in_bytes:
        assert decrypt(encrypted, in_pass + b"?") is None
