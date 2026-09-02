#!/usr/bin/env bash
# Snapshot all Git-tracked and non-ignored Hermes data, then push it.
set -euo pipefail

repo="/Users/deanradcliffe/.hermes"
cd "$repo"

git add -A

if git diff --cached --quiet; then
  exit 0
fi

git commit -m "chore: hourly Hermes data snapshot"
git push origin HEAD
