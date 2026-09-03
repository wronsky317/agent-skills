---
name: using-git-worktrees
description: Creates or verifies an isolated Git worktree without losing dirty work or confusing host-managed workspaces. Use when the user requests a worktree or isolated branch, or when an approved execution workflow requires isolation before substantial implementation.
---

# Using Git Worktrees

Detect existing isolation first, then create the smallest safe workspace only with user authorization.

## Workflow

1. **Inspect current state**
   - Run `git rev-parse --show-toplevel`, `git rev-parse --git-dir`, `git rev-parse --git-common-dir`, `git branch --show-current`, and `git status --short`.
   - A differing git dir/common dir can also indicate a submodule; check `git rev-parse --show-superproject-working-tree` before calling it a linked worktree.

2. **Respect workspace ownership**
   - If the host already provided an isolated or detached workspace, use it; do not nest another worktree.
   - If isolation was not requested or required by an active workflow, ask before creating one.
   - Prefer a host-native worktree mechanism when available.

3. **Choose a safe location**
   - Follow explicit repository/user conventions first.
   - Otherwise use an existing ignored `.worktrees/` or `worktrees/` directory.
   - Verify a project-local worktree directory is ignored before creation. Do not commit a `.gitignore` change unless authorized.

4. **Create the worktree**
   - Use a `codex/` branch prefix unless the user or repository specifies another prefix.
   - Never overwrite an existing path or branch.
   - Report the absolute worktree path and branch.

5. **Set up and verify baseline**
   - Run only repository-documented dependency/setup commands.
   - Run the smallest representative baseline tests before implementation.
   - If the baseline fails, separate pre-existing failures from new work and ask before proceeding when they compromise verification.

## Cleanup Boundary

The worktree's creator does not automatically own deletion. Remove it only after branch integration or explicit discard authorization, and never force removal over uncommitted files.

## Verification

- [ ] Existing host/worktree isolation was detected correctly.
- [ ] Creation was authorized and the target directory was safe and ignored.
- [ ] Branch and path were reported explicitly.
- [ ] Baseline setup/tests were recorded.
- [ ] No existing branch, worktree, or dirty file was overwritten.
