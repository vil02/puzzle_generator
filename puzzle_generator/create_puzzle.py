import inspect
import typing
import importlib.metadata

import black

from .puzzle_data_encryption import encrypt_data
from .configurators import configurators
from . import bytestr_utils


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


def _advertisement() -> str:
    package_name = "puzzle-generator"
    full_name = f"{package_name} {importlib.metadata.version(package_name)}"
    return f"""# generated with {full_name}
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator/
"""


def _split_long_str(in_str: str, max_len: int) -> typing.List[str]:
    if len(in_str) < max_len:
        return [in_str]
    return [in_str[:max_len]] + _split_long_str(in_str[max_len:], max_len)


def _str_to_code(in_str: str, max_len: int, quotes: str) -> str:
    return "\n".join(quotes + _ + quotes for _ in _split_long_str(in_str, max_len))


def _create_str(in_encrypted_puzzle, configurator) -> str:
    modules: str = "\n".join("import " + _ for _ in configurator.get_modules()) + "\n"
    objects: str = "\n".join(
        inspect.getsource(_) for _ in configurator.get_needed_objects()
    )
    question = _str_to_code(in_encrypted_puzzle[0], 78, '"""')
    rest_str = _str_to_code(
        bytestr_utils.bytes_to_bytestr(in_encrypted_puzzle[1]), 78, '"'
    )
    puzzle_data: str = f"_PUZZLE = ({question}, bytestr_to_bytes({rest_str}))"
    call: str = "run_puzzle(_PUZZLE, _DECRYPT, input)"

    return (
        "\n".join(
            [
                _advertisement(),
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
    res = _create_str(encrypted_puzzle, configurator)
    return black.format_str(res, mode=black.FileMode())
