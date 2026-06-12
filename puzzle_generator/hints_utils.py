import secrets
import typing


def compute_hint_to_index(
    hints: list[typing.Callable[[str], str] | None],
) -> tuple[
    list[typing.Callable[[str], str] | None],
    dict[typing.Callable[[str], str] | None, int],
]:
    unique_hints = list(set(hints))
    unique_hints.sort(key=lambda _: secrets.token_bytes())
    hint_to_index = {hint: idx for idx, hint in enumerate(unique_hints)}
    return unique_hints, hint_to_index
