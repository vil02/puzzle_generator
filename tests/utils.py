import itertools
import string
import typing

from puzzle_generator.encryption_algorithms.ea_simple import eas_simple, eas_spiced

STRS = [
    "",
    "some_STR?!",
    string.printable,
    string.whitespace,
    "ąęćśłńóżźĄĘĆŚŁŃÓŻŹ",
    "some_msg_with 🔨 and 🛷!",
    "🎮🎈🥅🐾 a🎄b",
    "🏀",
]

BYTES_LIST = [_.encode() for _ in STRS] + [b"\0", b"1235"]

SOME_SCRYPT_PARAMS = [
    {"salt": b"some_bad_salt", "n": 8, "r": 10, "p": 1},
    {"salt": b"some_other_bad_salt", "n": 16, "r": 20, "p": 1},
]

PROC_SPICES = [b"a", b"bb", b"ccc", b"dddd"]
SIGNATURE_SPICES = [b"XXX", b"YY", b"Z"]

_SOME_HASHES = [
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
]

SOME_SIGNATURE_PARAMS = [{"digest": _} for _ in _SOME_HASHES]


def _get_simple_encrypt_decrypt_pair(
    *args,
) -> tuple[
    typing.Callable[[bytes, bytes], bytes],
    typing.Callable[[bytes, bytes], bytes | None],
]:
    return eas_simple.get_encrypt(*args), eas_simple.get_decrypt(*args)


def _get_spiced_simple_encrypt_decrypt_pair(
    *args,
) -> tuple[
    typing.Callable[[bytes, bytes], bytes],
    typing.Callable[[bytes, bytes], bytes | None],
]:
    return eas_spiced.get_encrypt(*args), eas_spiced.get_decrypt(*args)


ENCRYPT_DECRYPT_PAIRS = [
    _get_simple_encrypt_decrypt_pair(scrypt_params, signature_params)
    for scrypt_params, signature_params in itertools.product(
        SOME_SCRYPT_PARAMS, SOME_SIGNATURE_PARAMS
    )
] + [
    _get_spiced_simple_encrypt_decrypt_pair(
        PROC_SPICES, SIGNATURE_SPICES, scrypt_params, signature_params
    )
    for scrypt_params, signature_params in itertools.product(
        SOME_SCRYPT_PARAMS, SOME_SIGNATURE_PARAMS
    )
]
