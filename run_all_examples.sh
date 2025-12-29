#!/usr/bin/env bash

set -euo pipefail

use_poetry=true

if [[ "${1:-}" == "--no-poetry" ]]; then
    use_poetry=false
fi
readonly use_poetry

function check_puzzle_code() {
    local puzzle_str="$1"
    readonly puzzle_str

    if ! echo -e "2\nPiotr" | python3 -c "${puzzle_str}"
    then
        return 1
    fi

    if echo -e "3" | python3 -c "${puzzle_str}"
    then
        return 2
    fi

    if echo -e "2\nWrong!" | python3 -c "${puzzle_str}"
    then
        return 3
    fi

    return 0
}

function check_example() {
    local example_file="$1"
    printf "Checking \"%s\"\n" "${example_file}"
    readonly example_file

    local puzzle_str
    if ${use_poetry}; then
        puzzle_str=$(poetry run python3 "${example_file}")
    else
        puzzle_str=$(python3 "${example_file}")
    fi
    readonly puzzle_str
    check_puzzle_code "${puzzle_str}"
    return 0
}

cd examples/

find . -name "*.py" | while read -r file; do
    check_example "${file}"
done
