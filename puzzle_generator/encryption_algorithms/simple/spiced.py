import typing
import secrets

from .common import (
    proc_bytes,
    hash_bytes,
    merge_encrypted_and_signature,
    split_encrypted_and_signature,
)


def get_encrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[bytes, bytes], bytes]:
    assert proc_spices
    assert signature_spices

    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        proc_spice = secrets.choice(proc_spices)
        signature_spice = secrets.choice(signature_spices)
        encrypted = proc_bytes(in_bytes, in_pass + proc_spice, proc_hasher)
        signature = hash_bytes(in_bytes + signature_spice, signature_hasher)
        return merge_encrypted_and_signature(encrypted, signature)

    return _encrypt


def get_decrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[bytes, bytes], bytes | None]:
    assert proc_spices
    assert signature_spices

    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        for proc_spice in proc_spices:
            encrypted, signature = split_encrypted_and_signature(
                in_bytes, signature_hasher().digest_size
            )
            res = proc_bytes(encrypted, in_pass + proc_spice, proc_hasher)

            if any(
                hash_bytes(res + _, signature_hasher) == signature
                for _ in signature_spices
            ):
                return res
        return None

    return _decrypt
