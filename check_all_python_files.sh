#!/usr/bin/env bash

set -euo pipefail

poetry run ruff check .
poetry run mypy .
find . -name "*.py" -exec ./check_python_file.sh {} +
