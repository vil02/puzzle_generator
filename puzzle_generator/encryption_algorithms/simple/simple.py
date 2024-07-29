import typing


from .common import (
    proc_bytes,
    hash_bytes,
    merge_encrypted_and_signature,
    split_encrypted_and_signature,
)


def get_encrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[bytes, bytes], bytes]:
    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        encrypted = proc_bytes(in_bytes, in_pass, proc_hasher)
        signature = hash_bytes(in_bytes, signature_hasher)
        return merge_encrypted_and_signature(encrypted, signature)

    return _encrypt


def get_decrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[bytes, bytes], bytes | None]:
    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        encrypted, signature = split_encrypted_and_signature(
            in_bytes, signature_hasher().digest_size
        )
        res = proc_bytes(encrypted, in_pass, proc_hasher)

        if hash_bytes(res, signature_hasher) == signature:
            return res
        return None

    return _decrypt
