import itertools
import typing

from .bytestr_utils import bytes_to_bytestr, bytestr_to_bytes


def hash_bytes(in_bytes: bytes, in_hasher) -> str:
    return str(in_hasher(in_bytes).hexdigest())


def int_to_bytes(in_val: int) -> bytes:
    return in_val.to_bytes((in_val.bit_length() + 7) // 8, "big")


def proc_bytes(in_bytes: bytes, in_key: bytes, in_hasher) -> bytes:
    """xors the in_bytes with a sequence of bytes generated with in_key"""
    key_bytes = itertools.chain.from_iterable(
        in_hasher(in_key + int_to_bytes(block_num)).digest()
        for block_num in itertools.count(0)
    )
    return bytes(_d ^ _k for (_d, _k) in zip(in_bytes, key_bytes))


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
