#!/usr/bin/env bash

set -euo pipefail

status=$(curl -s -X POST --data-binary @codecov.yml https://codecov.io/validate)
if [[ "${status}" == *Error* ]];
then
    printf "%s\n" "${status}"
    exit 1
fi
