import textwrap


def string_to_code(in_str: str, max_len: int, quotes: str) -> str:
    return "\n".join(
        quotes + line + quotes
        for line in textwrap.wrap(
            in_str,
            width=max_len,
            break_on_hyphens=False,
            replace_whitespace=False,
            drop_whitespace=False,
        )
    )
