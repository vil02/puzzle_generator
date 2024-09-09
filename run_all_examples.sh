#!/usr/bin/env bash

set -euo pipefail

use_poetry=true

if [[ "${1:-}" == "--no-poetry" ]]; then
    use_poetry=false
fi

cd examples/
if $use_poetry; then
    find . -name "*.py" -exec poetry run python3 {} +
else
    find . -name "*.py" -exec python3 {} +
fi
