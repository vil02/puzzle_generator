#!/usr/bin/env bash

set -euo pipefail

if [[ "$#" -ne 1 ]]; then
    echo "Provide one argument."
    exit 1
fi

VERSION_ARG=$1
readonly VERSION_ARG

poetry version "${VERSION_ARG}"


NEW_VERSION=$(poetry version --short)
readonly NEW_VERSION

git add pyproject.toml
git commit -m "chore: bump version to \`${NEW_VERSION}\`"
