#!/usr/bin/env bash
# Generate a digest issue and commit it. Extra args go to collect.py.
set -euo pipefail

cd "$(dirname "$0")/.."
python collect.py "$@"

git add -A content/posts content/full-log content/_index.md
if git diff --cached --quiet -- content/posts content/full-log content/_index.md; then
    echo "no post changes to commit"
    exit 0
fi

# Name the commit after the issue the run just wrote or refreshed.
post=$(git diff --cached --name-only --diff-filter=d -- content/posts | tail -1)
title=$(sed -n 's/^title: "\(.*\)"$/\1/p' "$post" | head -1)
git commit -q -m "${title:-Add digest issue}"
git --no-pager log -1 --oneline
