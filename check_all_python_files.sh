#!/usr/bin/env bash

set -euo pipefail

poetry run ruff check
poetry run ruff format
poetry run mypy .
poetry run pyright --warnings .
find . -name "*.py" -exec ./check_python_file.sh {} +
