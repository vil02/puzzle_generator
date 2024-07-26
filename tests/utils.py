import puzzle_generator.simple_encryption as se
import puzzle_generator.spiced_simple_encryption as sse


def get_simple_encrypt_decrypt_pair(*args):
    return se.get_encrypt(*args), se.get_decrypt(*args)


def get_spiced_simple_encrypt_decrypt_pair(*args):
    return sse.get_encrypt(*args), sse.get_decrypt(*args)
