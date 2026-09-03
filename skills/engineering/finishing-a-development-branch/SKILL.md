---
name: finishing-a-development-branch
description: Safely closes out completed branch work by re-verifying it and offering merge, pull-request, or keep-as-is choices. Use when implementation is complete and the user wants to integrate, publish, preserve, or clean up a development branch or worktree.
---

# Finishing a Development Branch

Verification comes before integration, and the user chooses what happens to the branch.

## Workflow

1. **Re-verify the exact tree**
   - Check status, branch, upstream, and worktree location.
   - Run the relevant full test/build suite on the tree that would be integrated.
   - Stop on failures; do not present the branch as ready.

2. **Determine provenance**
   - Identify the intended base from the plan, upstream, merge base, or conversation.
   - Confirm uncertain base-branch assumptions before merging.
   - Distinguish a normal checkout, owned linked worktree, and externally managed/detached workspace.

3. **Present safe choices**
   - Merge locally into the confirmed base.
   - Push and create a pull/merge request.
   - Keep the branch and workspace as-is.
   - Offer deletion only if the user explicitly asks to discard work.

4. **Execute only the selected choice**
   - Re-check remote/base state immediately before merge or push.
   - Never force-push, force-delete, or remove a dirty worktree without explicit authorization.
   - After a local merge, rerun tests on the merged result before cleanup.

5. **Clean up conservatively**
   - Remove only a worktree known to have been created for this task.
   - If removal reports untracked or modified files, show the exact files and ask whether to commit, move, or delete them.
   - Preserve worktrees used for an open pull request unless the user says otherwise.

## Suggested Choice Prompt

```text
Implementation is verified. What would you like to do?

1. Merge locally into <base>
2. Push and create a pull/merge request
3. Keep the branch as-is
```

## Verification

- [ ] Tests passed on the exact pre-integration tree.
- [ ] The base branch and workspace ownership were established.
- [ ] The user selected the integration action.
- [ ] Any merged result was tested again.
- [ ] Cleanup preserved all uncommitted and untracked work unless explicitly discarded.
