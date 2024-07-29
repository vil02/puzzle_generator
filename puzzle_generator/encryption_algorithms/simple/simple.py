import typing


from .common import (
    proc_bytes,
    hash_bytes,
    merge_data_and_signature,
    split_data_and_signature,
)


def get_encrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[bytes, bytes], bytes]:
    def _encrypt(in_bytes: bytes, in_pass: bytes) -> bytes:
        signature = hash_bytes(in_bytes, signature_hasher)
        merged = merge_data_and_signature(in_bytes, signature)
        return proc_bytes(merged, in_pass, proc_hasher)

    return _encrypt


def get_decrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[bytes, bytes], bytes | None]:
    def _decrypt(in_bytes: bytes, in_pass: bytes) -> bytes | None:
        data = proc_bytes(in_bytes, in_pass, proc_hasher)
        decrypted, signature = split_data_and_signature(
            data, signature_hasher().digest_size
        )

        if hash_bytes(decrypted, signature_hasher) == signature:
            return decrypted
        return None

    return _decrypt
