import pytest

import puzzle_generator.simple_encryption_utils as seu


@pytest.mark.parametrize(
    ("in_str", "in_pass"),
    [
        ("some_msg", "some_pass"),
        ("Ą", "other_pass!?#"),
        ("some_very_very_very_loooong_str", "ę"),
        ("ŁÓ", ""),
        ("", "a"),
        ("", ""),
        ("some_msg_with 🔨 and 🛷!", "?"),
        ("other message!@#$?", "a🎄b"),
        ("🎮🎈🥅🐾", "🏀"),
    ],
)
def test_seu(in_str, in_pass):
    encrypted, reshash = seu.encrypt_str(in_str, in_pass)
    if in_str:
        assert encrypted != in_str
    else:
        assert not encrypted
    decrypted = seu.decrypt_str(encrypted, in_pass, reshash)
    assert decrypted == in_str
    if in_str:
        assert seu.decrypt_str(encrypted, in_pass + "?", reshash) is None
