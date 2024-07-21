#!/usr/bin/env bash

set -euo pipefail

omitted_paths="tests/*"
readonly omitted_paths

poetry run coverage run --branch -m pytest
poetry run coverage xml --omit="${omitted_paths}"
poetry run coverage html --omit="${omitted_paths}"
poetry run coverage report --omit="${omitted_paths}"
