import typing


from .simple_encryption_utils import (
    proc_bytes,
    hash_bytes,
    merge_encrypted_and_signature,
    split_encrypted_and_signature,
)
from .bytestr_utils import bytes_to_bytestr, bytestr_to_bytes


def get_encrypt(proc_hasher, signature_hasher) -> typing.Callable[[str, str], str]:
    def _encrypt_bytes(in_bytes: bytes, in_pass: bytes) -> bytes:
        encrypted = proc_bytes(in_bytes, in_pass, proc_hasher)
        signature = hash_bytes(in_bytes, signature_hasher)
        return merge_encrypted_and_signature(encrypted, signature)

    def _encrypt(in_str: str, in_pass: str) -> str:
        encrypted = _encrypt_bytes(in_str.encode(), in_pass.encode())
        return bytes_to_bytestr(encrypted)

    return _encrypt


def get_decrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[str, str], str | None]:
    def _decrypt_bytes(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        encrypted, signature = split_encrypted_and_signature(
            in_bytes, signature_hasher().digest_size
        )
        res = proc_bytes(encrypted, in_pass, proc_hasher)

        if hash_bytes(res, signature_hasher) == signature:
            return res
        return None

    def _decrypt(in_str: str, in_pass: str) -> str | None:
        res = _decrypt_bytes(bytestr_to_bytes(in_str), in_pass.encode())
        if res is not None:
            return res.decode()
        return res

    return _decrypt
