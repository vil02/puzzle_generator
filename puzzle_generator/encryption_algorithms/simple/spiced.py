import typing
import secrets

from .common import (
    proc_bytes,
    hash_bytes,
    merge_data_and_signature,
    split_data_and_signature,
)


def get_encrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[bytes, bytes], bytes]:
    assert proc_spices  # nosec B101
    assert signature_spices  # nosec B101

    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature_spice = secrets.choice(signature_spices)
        signature = hash_bytes(in_bytes + signature_spice, signature_hasher)
        merged = merge_data_and_signature(in_bytes, signature)
        proc_spice = secrets.choice(proc_spices)
        return proc_bytes(merged, in_pass + proc_spice, proc_hasher)

    return _encrypt


def get_decrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[bytes, bytes], bytes | None]:
    assert proc_spices  # nosec B101
    assert signature_spices  # nosec B101

    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        for proc_spice in proc_spices:
            data = proc_bytes(in_bytes, in_pass + proc_spice, proc_hasher)
            decrypted, signature = split_data_and_signature(
                data, signature_hasher().digest_size
            )

            if any(
                hash_bytes(decrypted + _, signature_hasher) == signature
                for _ in signature_spices
            ):
                return decrypted
        return None

    return _decrypt
