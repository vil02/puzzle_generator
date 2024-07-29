import string

import puzzle_generator.encryption_algorithms.simple.simple as se
import puzzle_generator.encryption_algorithms.simple.spiced as sse


def get_simple_encrypt_decrypt_pair(*args):
    return se.get_encrypt(*args), se.get_decrypt(*args)


def get_spiced_simple_encrypt_decrypt_pair(*args):
    return sse.get_encrypt(*args), sse.get_decrypt(*args)


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
