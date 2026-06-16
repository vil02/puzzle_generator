import typing

BYTEORDER: typing.Literal["little", "big"] = "little"


def byte_length(in_value: int) -> int:
    if in_value < 0:
        raise ValueError("in_value must be non-negative")
    number_of_bytes = in_value.bit_length() // 8
    if 8 * number_of_bytes < in_value.bit_length():
        number_of_bytes += 1
    return number_of_bytes


def int_to_bytes(in_value: int) -> bytes:
    number_of_bytes = byte_length(in_value)
    if number_of_bytes > 255:
        raise ValueError("in_value must be 255 bytes or less")
    return number_of_bytes.to_bytes(length=1, byteorder=BYTEORDER) + in_value.to_bytes(
        length=number_of_bytes, byteorder=BYTEORDER
    )


def bytes_to_int(in_bytes: bytes) -> int:
    bytes_length = int(in_bytes[0])
    if len(in_bytes) != bytes_length + 1:
        raise ValueError("in_bytes has wrong structure")
    return int.from_bytes(in_bytes[1:], byteorder=BYTEORDER)


def join_bytes_blocks(bytes_a: bytes, bytes_b: bytes) -> bytes:
    return int_to_bytes(len(bytes_a)) + bytes_a + bytes_b


def join(in_str: str, in_bytes: bytes) -> bytes:
    return join_bytes_blocks(in_str.encode(), in_bytes)


def split_bytes_blocks(in_bytes: bytes) -> tuple[bytes, bytes]:
    end_of_length = int(in_bytes[0]) + 1
    bytes_a_len = bytes_to_int(in_bytes[:end_of_length])
    end_of_bytes_a = end_of_length + bytes_a_len
    bytes_a = in_bytes[end_of_length:end_of_bytes_a]
    bytes_b = in_bytes[end_of_bytes_a:]
    return bytes_a, bytes_b


def split(in_bytes: bytes) -> tuple[str, bytes]:
    str_as_bytes, res_bytes = split_bytes_blocks(in_bytes)
    return str_as_bytes.decode(), res_bytes


def join_with_hints(in_str: str, in_index: int, in_bytes: bytes) -> bytes:
    return join(in_str, join_bytes_blocks(int_to_bytes(in_index), in_bytes))


def split_with_hints(in_bytes: bytes) -> tuple[str, int, bytes]:
    res_str, index_and_res_bytes = split(in_bytes)
    index_as_bytes, res_bytes = split_bytes_blocks(index_and_res_bytes)
    return res_str, bytes_to_int(index_as_bytes), res_bytes
