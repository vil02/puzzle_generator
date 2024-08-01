#!/usr/bin/env bash

set -euo pipefail

cd examples/
find . -name "*.py" -exec poetry run python3 {} +
