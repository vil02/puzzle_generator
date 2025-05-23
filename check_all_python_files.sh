#!/usr/bin/env bash

set -euo pipefail

poetry run ruff check .
poetry run mypy .
poetry run bandit -c bandit.yml -r .
poetry run isort --profile black --check .
find . -name "*.py" -exec ./check_python_file.sh {} +
