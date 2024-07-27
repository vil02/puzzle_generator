#!/bin/bash

set -euo pipefail

current_branch=$(git branch --show-current)
readonly current_branch
if [[ "${current_branch}" != "master" ]]; then
    echo "You are not on the master."
    exit 1
fi

current_version=$(poetry version --short)
readonly current_version
if [[ -z "${current_version}" ]]; then
    echo "Failed to get the current version from poetry."
    exit 1
fi

tag_name="v${current_version}"
readonly tag_name
if git ls-remote --tags origin | grep "refs/tags/${tag_name}"; then
    echo "Tag ${tag_name} already exists."
    exit 0
fi

git tag "${tag_name}"
git push origin tag "${tag_name}"
