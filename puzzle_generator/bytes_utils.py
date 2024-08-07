import typing


BYTEORDER: typing.Literal["little", "big"] = "little"


def int_to_bytes(in_value: int) -> bytes:
    if in_value < 0:
        raise ValueError("in_value must be non-negative")
    number_of_bytes = get_num_bytes(in_value)
    if number_of_bytes > 255:
        raise ValueError("in_value must be 255 bytes or less")
    return number_of_bytes.to_bytes(length=1, byteorder=BYTEORDER) + in_value.to_bytes(
        length=number_of_bytes, byteorder=BYTEORDER
    )


def byte_length(in_value):
    number_of_bytes = in_value.bit_length() // 8
    if 8 * number_of_bytes < in_value.bit_length():
        number_of_bytes += 1
    return number_of_bytes


def bytes_to_int(in_bytes: bytes) -> int:
    bytes_length = int(in_bytes[0])
    assert len(in_bytes) == bytes_length + 1  # nosec B101
    return int.from_bytes(in_bytes[1:], byteorder=BYTEORDER)


def join(in_str: str, in_bytes: bytes) -> bytes:
    str_as_bytes = in_str.encode()
    return int_to_bytes(len(str_as_bytes)) + str_as_bytes + in_bytes


def split(in_bytes: bytes) -> typing.Tuple[str, bytes]:
    end_of_length = int(in_bytes[0]) + 1
    str_as_bytes_len = bytes_to_int(in_bytes[:end_of_length])
    end_of_str = end_of_length + str_as_bytes_len
    str_as_bytes = in_bytes[end_of_length:end_of_str]
    res_bytes = in_bytes[end_of_str:]
    return str_as_bytes.decode(), res_bytes
