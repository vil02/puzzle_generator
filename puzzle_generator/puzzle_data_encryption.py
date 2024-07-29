import typing

from .bytes_utils import join, split


def encrypt_data(
    in_data, in_encrypt: typing.Callable[[bytes, bytes], bytes]
) -> typing.Tuple[str, bytes]:
    if list(in_data.keys()) == ["str"]:
        return in_data["str"], bytes()
    tmp = encrypt_data(in_data["rest"], in_encrypt)
    rest = join(tmp[0], tmp[1])
    encrypted = in_encrypt(rest, in_data["pass"].encode())
    return in_data["str"], encrypted


def decrypt_data(
    in_rest: bytes,
    in_pass: str,
    in_decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None | typing.Tuple[str, bytes]:
    res = in_decrypt(in_rest, in_pass.encode())
    if res is None:
        return None
    return split(res)
