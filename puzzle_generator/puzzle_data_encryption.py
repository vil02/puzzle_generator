import typing


def encrypt_data(in_data, in_encrypt: typing.Callable[[str, str], str]):
    if list(in_data.keys()) == ["str"]:
        return [in_data["str"]]
    rest: str = str(encrypt_data(in_data["rest"], in_encrypt))[1:-1]
    encrypted: str = in_encrypt(rest, in_data["pass"])
    return [in_data["str"], encrypted]


def decrypted_data_to_list(in_data: str) -> typing.List[str]:
    pieces = in_data.split("', '")
    if len(pieces) == 2:
        assert pieces[0][0] == "'"
        assert pieces[1][-1] == "'"
        return [pieces[0][1:], pieces[1][:-1]]
    assert len(pieces) == 1
    return [pieces[0][1:-1]]


def decrypt_data(
    in_rest: str, in_pass: str, in_decrypt: typing.Callable[[str, str], str | None]
):
    rest_str = in_decrypt(in_rest, in_pass)
    if rest_str is None:
        return None
    return decrypted_data_to_list(rest_str)
