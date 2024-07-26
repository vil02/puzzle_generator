import typing

from .simple_encryption_utils import proc_bytes, hash_bytes
from .bytestr_utils import bytes_to_bytestr, bytestr_to_bytes


def get_encrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[str, str], typing.Tuple[str, str]]:
    def _encrypt_bytes(in_bytes: bytes, in_pass: bytes) -> typing.Tuple[bytes, str]:
        return proc_bytes(in_bytes, in_pass, proc_hasher), hash_bytes(
            in_bytes, signature_hasher
        )

    def _encrypt(in_str: str, in_pass: str) -> typing.Tuple[str, str]:
        encrypted_bytes, hash_str = _encrypt_bytes(in_str.encode(), in_pass.encode())
        return bytes_to_bytestr(encrypted_bytes), hash_str

    return _encrypt


def get_decrypt(
    proc_hasher, signature_hasher
) -> typing.Callable[[str, str, str], str | None]:
    def _decrypt_bytes(in_bytes: bytes, in_pass: bytes, in_hash: str) -> bytes | None:
        res = proc_bytes(in_bytes, in_pass, proc_hasher)

        if hash_bytes(res, signature_hasher) == in_hash:
            return res
        return None

    def _decrypt(in_str: str, in_pass: str, in_hash: str) -> str | None:
        res = _decrypt_bytes(bytestr_to_bytes(in_str), in_pass.encode(), in_hash)
        if res is not None:
            return res.decode()
        return res

    return _decrypt
