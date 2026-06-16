import base64


def bytes_to_bytestr(in_bytes: bytes) -> str:
    return base64.standard_b64encode(in_bytes).decode("utf-8")


def bytestr_to_bytes(in_str: str) -> bytes:
    return base64.standard_b64decode(in_str)
