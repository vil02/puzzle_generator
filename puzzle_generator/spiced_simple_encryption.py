import typing
import secrets

from .simple_encryption_utils import proc_bytes, hash_bytes
from .bytestr_utils import bytes_to_bytestr, bytestr_to_bytes


def get_encrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[str, str], typing.Tuple[str, str]]:
    assert proc_spices
    assert signature_spices

    def _encrypt_bytes(in_bytes: bytes, in_pass: bytes) -> typing.Tuple[bytes, str]:
        proc_spice = secrets.choice(proc_spices)
        signature_spice = secrets.choice(signature_spices)
        return proc_bytes(in_bytes, in_pass + proc_spice, proc_hasher), hash_bytes(
            in_bytes + signature_spice, signature_hasher
        )

    def _encrypt(in_str: str, in_pass: str) -> typing.Tuple[str, str]:
        encrypted_bytes, hash_str = _encrypt_bytes(in_str.encode(), in_pass.encode())
        return bytes_to_bytestr(encrypted_bytes), hash_str

    return _encrypt


def get_decrypt(
    proc_hasher,
    signature_hasher,
    proc_spices: typing.List[bytes],
    signature_spices: typing.List[bytes],
) -> typing.Callable[[str, str, str], str | None]:
    assert proc_spices
    assert signature_spices

    def _decrypt_bytes(in_bytes: bytes, in_pass: bytes, in_hash: str) -> bytes | None:
        for proc_spice in proc_spices:
            res = proc_bytes(in_bytes, in_pass + proc_spice, proc_hasher)

            if any(
                hash_bytes(res + _, signature_hasher) == in_hash
                for _ in signature_spices
            ):
                return res
        return None

    def _decrypt(in_str: str, in_pass: str, in_hash: str) -> str | None:
        res = _decrypt_bytes(bytestr_to_bytes(in_str), in_pass.encode(), in_hash)
        if res is not None:
            return res.decode()
        return res

    return _decrypt
