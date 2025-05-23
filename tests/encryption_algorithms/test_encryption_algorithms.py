import typing

import pytest

from .. import utils


@pytest.mark.parametrize("in_bytes", utils.BYTES_LIST)
@pytest.mark.parametrize("in_pass", utils.BYTES_LIST)
@pytest.mark.parametrize(("encrypt", "decrypt"), utils.ENCRYPT_DECRYPT_PAIRS)
def test_encryption_decryption(
    in_bytes: bytes,
    in_pass: bytes,
    encrypt: typing.Callable[[bytes, bytes], bytes],
    decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None:
    encrypted = encrypt(in_bytes, in_pass)

    assert encrypted != in_bytes
    decrypted = decrypt(encrypted, in_pass)
    assert decrypted == in_bytes
    if in_bytes:
        assert decrypt(encrypted, in_pass + b"?") is None
