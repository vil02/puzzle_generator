import inspect
import typing

from .puzzle_data_encryption import encrypt_data
from .configurators import configurators
from .encryption_algorithms import bytestr_utils


def question_answer_list_to_dict(qa_list: typing.List[str]):
    if len(qa_list) % 2 == 0:
        raise ValueError("The question/answer list must have odd length.")
    if len(qa_list) == 1:
        return {"str": qa_list[0]}
    return {
        "str": qa_list[0],
        "pass": qa_list[1],
        "rest": question_answer_list_to_dict(qa_list[2:]),
    }


def _create_str(in_encrypted_puzzle, configurator) -> str:
    advertisement = """# generated with puzzle-generator
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator/
"""
    modules: str = "\n".join("import " + _ for _ in configurator.get_modules()) + "\n"
    objects: str = "\n".join(
        inspect.getsource(_) for _ in configurator.get_needed_objects()
    )
    question = in_encrypted_puzzle[0]
    rest_str = bytestr_utils.bytes_to_bytestr(in_encrypted_puzzle[1])
    puzzle_data: str = f'_PUZZLE = ("{question}", bytestr_to_bytes("{rest_str}"))'
    call: str = "run_puzzle(_PUZZLE, _DECRYPT, input)"

    return (
        "\n".join(
            [
                advertisement,
                modules,
                'BYTEORDER: typing.Literal["little", "big"] = "little"',
                objects,
                puzzle_data,
                configurator.get_constants_str(),
                call,
            ]
        )
        + "\n"
    )


def create(qa_list: typing.List[str], **kwargs) -> str:
    puzzle = question_answer_list_to_dict(qa_list)
    configurator = configurators.get_configurator(**kwargs)
    encrypted_puzzle = encrypt_data(puzzle, configurator.get_encrypt())
    return _create_str(encrypted_puzzle, configurator)
