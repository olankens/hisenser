#!/bin/bash

set -euo pipefail

GITHUB_USER="olankens"
GITHUB_NAME="hisenser"
README_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/README.md"

FOR_REPLACE="https://github.com/${GITHUB_USER}/${GITHUB_NAME}/raw/HEAD/.github/assets/"
[[ -f "$README_FILE" ]] && perl -0pi -e "s|\"${FOR_REPLACE}|\".github/assets/|g" "$README_FILE"
