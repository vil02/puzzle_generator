import itertools
import typing
import hashlib

from .bytestr_utils import bytes_to_bytestr, bytestr_to_bytes


def hash_bytes(in_bytes: bytes) -> str:
    return hashlib.sha512(in_bytes).hexdigest()


def int_to_bytes(in_val: int) -> bytes:
    return in_val.to_bytes((in_val.bit_length() + 7) // 8, "big")


def proc_bytes(in_bytes: bytes, in_key: bytes) -> bytes:
    """xors the in_bytes with a sequence of bytes generated with in_key"""
    key_bytes = itertools.chain.from_iterable(
        hashlib.sha512(in_key + int_to_bytes(block_num)).digest()
        for block_num in itertools.count(0)
    )
    return bytes(_d ^ _k for (_d, _k) in zip(in_bytes, key_bytes))


def encrypt_bytes(in_bytes: bytes, in_pass: bytes) -> typing.Tuple[bytes, str]:
    return proc_bytes(in_bytes, in_pass), hash_bytes(in_bytes)


def decrypt_bytes(in_bytes: bytes, in_pass: bytes, in_hash: str) -> bytes | None:
    res = proc_bytes(in_bytes, in_pass)

    if hash_bytes(res) == in_hash:
        return res
    return None


def encrypt_str(in_str: str, in_pass: str) -> typing.Tuple[str, str]:
    """encrypts in_str using in_pass"""
    encrypted_bytes, hash_str = encrypt_bytes(in_str.encode(), in_pass.encode())
    return bytes_to_bytestr(encrypted_bytes), hash_str


def decrypt_str(in_str: str, in_pass: str, in_hash: str) -> str | None:
    res = decrypt_bytes(bytestr_to_bytes(in_str), in_pass.encode(), in_hash)
    if res is not None:
        return res.decode()
    return res
