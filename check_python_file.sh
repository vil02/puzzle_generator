#!/usr/bin/env bash

set -euo pipefail

declare -i exit_code=0

for cur_file in "$@"
do
    mypy_output=$(poetry run mypy "${cur_file}" 2>&1) || {
        printf "Checking with mypy:\n%s\n" "${mypy_output}"
        exit_code=1
    }

    xenon_output=$(poetry run xenon --max-absolute A --max-modules A --max-average A "${cur_file}" 2>&1) || {
        printf "Checking with xenon:\n%s\n" "${xenon_output}"
        exit_code=1
    }
done

if [[ ${exit_code} -eq 0 ]] ; then
   printf "\nNo errors found!\n"
fi

exit "${exit_code}"
