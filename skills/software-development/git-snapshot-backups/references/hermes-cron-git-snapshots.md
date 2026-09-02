# Hermes Cron Git Snapshot Notes

## Tested scheduler pattern

A `cronjob_manage` job configured with:

- `schedule: "0 * * * *"`
- `script: <script name relative to ~/.hermes/scripts/>`
- `no_agent: true`
- `workdir: <absolute repository root>`
- `deliver: local`

runs the shell script directly on the hour. In `no_agent` mode, empty stdout sends no routine delivery; non-zero exits are recorded as failures. A manually triggered `run` starts in the background and its outcome is delivered back into the conversation—do not poll it.

## Scoped snapshot script shape

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$repo"
git add -A
if git diff --cached --quiet; then
  exit 0
fi
git commit -m "chore: hourly data snapshot"
git push origin HEAD
```

This shape is safe only after `.gitignore` has been audited. It stages every non-ignored file, not merely files a human would call user-facing.

## Repairing an oversized pushed snapshot

1. Add targeted generated-artifact exclusions to `.gitignore`.
2. Run `git rm -r --cached <excluded-path>`; this removes index entries without deleting the local generated files.
3. Stage the ignore rule and amend the local snapshot.
4. Verify excluded files have zero entries in `git ls-tree -r --name-only HEAD -- <excluded-path>` and inspect the amended commit summary.
5. Ask for immediate user confirmation before `git push --force-with-lease origin HEAD:<branch>`.
6. Verify the remote ref equals the local `HEAD` after pushing.
