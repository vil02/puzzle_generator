#!/usr/bin/env bash

set -euo pipefail

find . -name "*.py" -exec ./check_python_file.sh {} +
