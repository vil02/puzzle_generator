import inspect
import textwrap
import typing
import importlib.metadata

import black

from .puzzle_data_encryption import encrypt_data
from .puzzle_data_creators import question_answer_list_to_dict
from .configurators import configurators
from . import rp_configurators
from . import bytestr_utils


def _advertisement() -> str:
    package_name = "puzzle-generator"
    full_name = f"{package_name} {importlib.metadata.version(package_name)}"
    return f"""# generated with {full_name}
#
# https://pypi.org/project/puzzle-generator/
# https://github.com/vil02/puzzle_generator/
"""


def _str_to_code(in_str: str, max_len: int, quotes: str) -> str:
    return "\n".join(
        quotes + line + quotes
        for line in textwrap.wrap(
            in_str,
            width=max_len,
            replace_whitespace=False,  # Preserves embedded whitespace like `\n`
            drop_whitespace=False,  # Keeps leading/trailing spaces
        )
    )


def _create_str(in_encrypted_puzzle, configurator, rp_configurator) -> str:
    modules: str = "\n".join("import " + _ for _ in configurator.get_modules()) + "\n"
    objects: str = "\n".join(
        inspect.getsource(_)
        for _ in configurator.get_needed_objects()
        + rp_configurator.get_needed_objects()
    )
    question = _str_to_code(in_encrypted_puzzle[0], 78, '"""')
    rest_str = _str_to_code(
        bytestr_utils.bytes_to_bytestr(in_encrypted_puzzle[1]), 78, '"'
    )

    return (
        "\n".join(
            [
                _advertisement(),
                modules,
                'BYTEORDER: typing.Literal["little", "big"] = "little"',
                objects,
                rp_configurator.puzzle_data(question, rest_str),
                configurator.get_constants_str(),
                rp_configurator.call(),
            ]
        )
        + "\n"
    )


def extract_qa_list_and_hints(
    puzzle_description: typing.Sequence[
        tuple[str, str, typing.Callable[[str], str] | None] | str
    ],
) -> tuple[list[str], list[typing.Callable[[str], str] | None]]:
    qa_list: list[str] = []
    hints: list[typing.Callable[[str], str] | None] = []
    for _ in puzzle_description[:-1]:
        question, answer, hint = _
        qa_list += [question, answer]
        hints.append(hint)
    if not isinstance(puzzle_description[-1], str):
        raise ValueError(
            "In case of puzzle with hints, "
            "the last entry of the puzzle_description must be a string"
        )
    qa_list.append(puzzle_description[-1])
    return qa_list, hints


def create(
    puzzle_description: (
        list[str]
        | typing.Sequence[tuple[str, str, typing.Callable[[str], str] | None] | str]
    ),
    **kwargs,
) -> str:
    if isinstance(puzzle_description, list) and all(
        isinstance(_, str) for _ in puzzle_description
    ):
        qa_list: list[str] = puzzle_description
        hints: list[typing.Callable[[str], str] | None] = [
            None for _ in range(len(qa_list) // 2 + 1)
        ]
    else:
        qa_list, hints = extract_qa_list_and_hints(puzzle_description)

    puzzle = question_answer_list_to_dict(qa_list)
    configurator = configurators.get_configurator(**kwargs)
    encrypted_puzzle = encrypt_data(puzzle, configurator.get_encrypt())
    res = _create_str(
        encrypted_puzzle, configurator, rp_configurators.get_rp_configurator(hints)
    )
    return black.format_str(res, mode=black.FileMode())
