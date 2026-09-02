---
name: git-snapshot-backups
description: Use when scheduling Git backups. Safely stage and sync.
version: 0.1.0
author: Dean Radcliffe, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Git, backup, snapshots, cron, recovery]
    related_skills: []
---

# Git Snapshot Backups

Use this skill to create or repair scheduled Git backups of user-facing data. It focuses on bounded staging, verifiable remote synchronization, and recoverable remediation—not treating every unignored file as meaningful data.

## When to Use

- A user wants periodic commits and pushes of an application-data or workspace repository.
- A cron-driven Git snapshot must be tested, audited, or repaired after an unintended commit.
- A backup repository mixes user data with caches, generated dependencies, runtime state, or credentials.

Do not use this for ordinary source-control workflows, release commits, or unreviewed history rewrites.

## Prerequisites

- Use `terminal` to verify the repository root, working-tree status, current branch, and `origin` before changing anything.
- Use `read_file` to inspect `.gitignore`; do not inspect credential files. Confirm that known secrets such as `.env` and authentication material are excluded.
- For Hermes cron configuration, load the `hermes-agent` skill and its background-systems reference before creating or changing a job.

## Procedure

1. **Audit the staging boundary.** Run `git status --short`, group untracked paths by top-level directory, and inspect `.gitignore`. Identify generated dependency trees, caches, locks, logs, and runtime artifacts before using broad staging. Completion: each category is deliberately included or ignored.
2. **Define the backup script.** Create a small script that changes into the verified repository, stages the approved boundary, exits silently when there is no staged change, commits with a clear snapshot message, then pushes the intended branch to `origin`. Use `set -euo pipefail`. Completion: the script passes a shell syntax check.
3. **Make broad staging safe before automation.** If using `git add -A`, encode exclusions in `.gitignore` first. An ignore rule does not untrack files already in history; remove those from the index with `git rm -r --cached <path>` while leaving local files intact. Completion: `git ls-tree -r --name-only HEAD -- <excluded-path>` returns zero after the cleanup commit.
4. **Create a script-only cron job.** Prefer `cronjob_manage` with `no_agent: true`, the validated script, an explicit cron expression such as `0 * * * *` for on-the-hour execution, and `deliver: local` for a quiet backup. List jobs first to avoid duplicates. Completion: read the job back and confirm its schedule, script, workdir, enabled state, and next run.
5. **Test once before relying on the schedule.** Trigger the job with `cronjob_manage(action='run')`. It runs in the background; do not poll. When its result returns, verify the local commit, working tree, and the exact remote branch hash with `git ls-remote`. Completion: local and remote hashes match, or the failure is surfaced with its cause.
6. **Repair an accidental remote snapshot deliberately.** First amend ignores and clean the local index; then amend or replace the local commit and verify its scope. If the bad commit was already pushed, ask the user for explicit confirmation immediately before `git push --force-with-lease`. Completion: only after confirmation, verify the remote ref equals the corrected local hash.

## Pitfalls

- `git add -A` means every non-ignored artifact, including dependency directories such as `node_modules`; it is not synonymous with “user-facing data.”
- `.gitignore` prevents future untracked additions but does not remove already tracked paths.
- Never force-push an automated backup repair without explicit, immediate user confirmation. Prefer `--force-with-lease` over `--force`.
- A successful push command is not verification. Read the exact remote ref after each external write.
- Keep routine no-change runs quiet: an empty script stdout in Hermes `no_agent` cron mode sends no delivery.

## Verification

- The backup script has passed its syntax check.
- The cron job exists exactly once and is enabled with the requested schedule.
- A manual test produced either no commit for a clean repository or one scoped snapshot commit.
- `git rev-parse HEAD` and `git ls-remote origin refs/heads/<branch>` agree after a push.
- Excluded generated paths are absent from the Git tree and stay excluded on a subsequent `git add -A`.

See `references/hermes-cron-git-snapshots.md` for the Hermes scheduler behavior and a tested recovery sequence.
