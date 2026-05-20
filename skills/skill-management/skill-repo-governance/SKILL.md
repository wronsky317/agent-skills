---
name: skill-repo-governance
description: Audits and maintains the shared skill repository, including skill structure, trigger descriptions, progressive disclosure, duplicate coverage, validation scripts, and quality gates. Use when updating /Users/wronsky/Documents/agent-skills, reviewing existing skills, adding repository-wide skill standards, deduplicating skills, or validating SKILL.md files.
---

# Skill Repo Governance

Use this skill to keep the shared skill repository coherent. The goal is not to maximize the number of skills; it is to keep each skill discoverable, scoped, executable, and easy to maintain.

## Governance Workflow

1. **Inventory first**
   - List all `skills/**/SKILL.md` files.
   - Read the skills that overlap with the requested change.
   - Check `git status --short` before editing.
   - Do not modify generated, imported, or unrelated skills unless the task requires it.

2. **Map intent to existing coverage**
   - Prefer updating an existing skill when the new workflow is a variant of current behavior.
   - Create a new skill only when it has a distinct trigger, workflow, or reusable resource set.
   - If two skills would trigger for the same request, either merge them or make their descriptions disjoint.

3. **Design for progressive disclosure**
   - Keep `SKILL.md` focused on the activation rule, decision path, core workflow, and verification.
   - Move long examples, detailed standards, checklists, and inventories into `references/`.
   - Keep references one level deep from `SKILL.md`.
   - Add `scripts/` only for deterministic, reusable operations.
   - Do not create empty resource directories.

4. **Validate trigger metadata**
   - `name` must match the skill directory name.
   - `description` must say both what the skill does and when to use it.
   - Put trigger terms in `description`, not only in the body.
   - Keep description under 1024 characters.
   - Avoid vague names such as `helper`, `workflow`, or `tools`.

5. **Require an executable workflow**
   - Every maintained skill should have a concrete process, not just advice.
   - Prefer sections named `Workflow`, `Process`, `Procedure`, or `Steps`.
   - Include what evidence proves completion: command output, rendered artifact, test result, screenshot, diff review, or explicit residual risk.

6. **Run validation**
   - Run `python3 scripts/validate-skills.py` from the repository root after structure changes.
   - Treat errors as blockers.
   - Treat warnings as a cleanup queue unless the user asked for strict cleanup.

## Skill Quality Bar

Use these checks before finalizing a new or updated skill:

- **Specific**: the workflow tells the agent what to do next, not only what to care about.
- **Discoverable**: the description contains likely user phrasing and task contexts.
- **Scoped**: the skill has a clear boundary and does not absorb unrelated workflows.
- **Verifiable**: the skill defines evidence required before reporting success.
- **Token-conscious**: detail that is not always needed lives in references.
- **Non-duplicative**: it references adjacent skills instead of copying their full content.

## Anti-Rationalization Checks

| Rationalization | Reality |
|---|---|
| "This is useful, so it should be a new skill." | Usefulness is not enough. It needs a distinct trigger and repeated workflow. |
| "The body explains when to use it." | The body is loaded after triggering. Trigger conditions must be in `description`. |
| "A long SKILL.md is fine because the content is good." | Long skills tax every triggered use. Move detail to references. |
| "An empty scripts directory signals future intent." | Empty directories add noise. Add `scripts/` only with runnable helpers. |
| "Warnings can be ignored forever." | Warnings are technical debt. Track them or intentionally accept them. |

## References

- Read [references/skill-anatomy.md](references/skill-anatomy.md) when creating or heavily rewriting a skill.
- Read [references/orchestration-patterns.md](references/orchestration-patterns.md) when changing how skills, personas, commands, or multi-agent flows compose.

## Verification

Before finishing repository governance work, confirm:

- [ ] `git status --short` was checked before editing.
- [ ] New or updated descriptions include both capability and trigger context.
- [ ] Related skills were checked for overlap.
- [ ] `python3 scripts/validate-skills.py` was run, or the reason it could not run is reported.
- [ ] Any remaining warnings or skipped validations are reported to the user.
