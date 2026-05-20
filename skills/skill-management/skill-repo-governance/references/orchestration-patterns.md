# Orchestration Patterns

Use this reference when a change affects how skills, personas, commands, or multi-agent work compose.

## Layers

Keep these responsibilities separate:

| Layer | Responsibility | Example |
|---|---|---|
| Skill | The workflow: steps, rules, verification | `code-review`, `qa`, `create-skill` |
| Persona | A viewpoint or role with output expectations | reviewer, security auditor, test engineer |
| Command | A user-facing entry point or shortcut | `/review`, `/ship` |
| Script | Deterministic helper code | validators, scaffolders, parsers |

Do not hide routing logic inside a persona. The user, command, or main agent should choose the workflow.

## Preferred Patterns

### Sequential lifecycle

Use when later work depends on earlier decisions.

```text
discover -> design -> implement -> verify -> review
```

Example: creating a new skill should normally follow `create-skill`, then `skill-repo-governance`, then validator checks.

### Parallel fan-out

Use only when independent reviewers can inspect the same artifact without mutating shared state.

```text
main agent
  -> reviewer A
  -> reviewer B
  -> reviewer C
main agent merges reports
```

Good for review, security audit, and test coverage analysis. Avoid it for tightly coupled implementation work unless write scopes are disjoint.

### Reference handoff

Use when one skill owns the workflow but needs detailed standards.

```text
SKILL.md -> references/specific-guide.md
```

The main skill should say exactly when to read the reference.

## Anti-Patterns

- Router personas that only decide which other persona to call.
- Skills that duplicate another skill's full body instead of linking to it.
- Commands that bypass required verification.
- Multiple skills with indistinguishable trigger descriptions.
- Scripts that silently mutate repository state without reporting changed files.

## Verification

When changing orchestration, verify:

- [ ] Each layer has a single clear responsibility.
- [ ] Trigger descriptions do not overlap unintentionally.
- [ ] Any parallel work is read-only or has disjoint write scopes.
- [ ] Merge or final reporting responsibility is explicit.
- [ ] The user can tell which workflow ran and what evidence it produced.
