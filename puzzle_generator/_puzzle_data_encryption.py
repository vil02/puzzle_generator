import typing

from ._bytes_utils import join, join_with_hints, split, split_with_hints


def encrypt_data(
    in_data, in_encrypt: typing.Callable[[bytes, bytes], bytes]
) -> tuple[str, bytes]:
    if list(in_data.keys()) == ["str"]:
        return in_data["str"], b""
    tmp = encrypt_data(in_data["rest"], in_encrypt)
    rest = join(tmp[0], tmp[1])
    encrypted = in_encrypt(rest, in_data["pass"].encode())
    return in_data["str"], encrypted


def decrypt_data(
    in_rest: bytes,
    in_pass: str,
    in_decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None | tuple[str, bytes]:
    res = in_decrypt(in_rest, in_pass.encode())
    if res is None:
        return None
    return split(res)


def encrypt_data_with_hints(
    in_data, in_encrypt: typing.Callable[[bytes, bytes], bytes]
) -> tuple[str, int, bytes]:
    if list(in_data.keys()) == ["str"]:
        return in_data["str"], 0, b""
    tmp = encrypt_data_with_hints(in_data["rest"], in_encrypt)
    rest = join_with_hints(tmp[0], tmp[1], tmp[2])
    encrypted = in_encrypt(rest, in_data["pass"].encode())
    return in_data["str"], in_data["index"], encrypted


def decrypt_data_with_hints(
    in_rest: bytes,
    in_pass: str,
    in_decrypt: typing.Callable[[bytes, bytes], bytes | None],
) -> None | tuple[str, int, bytes]:
    res = in_decrypt(in_rest, in_pass.encode())
    if res is None:
        return None
    return split_with_hints(res)
