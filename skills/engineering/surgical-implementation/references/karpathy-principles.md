# Karpathy-Inspired Coding Agent Principles

This reference preserves attribution and rationale for the `surgical-implementation` skill. The main skill should stay workflow-focused; load this file only when source context or deeper rationale is useful.

## Attribution

The workflow is inspired by Andrej Karpathy's public observations about common LLM coding failure modes: silent assumptions, unmanaged confusion, overcomplicated implementations, unrelated edits, and weak success criteria.

Local source analyzed before distillation:

- Repository: `/Users/wronsky/Documents/skill-codebases/andrej-karpathy-skills`
- Skill file: `/Users/wronsky/Documents/skill-codebases/andrej-karpathy-skills/skills/karpathy-guidelines/SKILL.md`

## Distilled Mapping

| Principle | Implementation behavior |
|---|---|
| Think before coding | Restate the goal, expose assumptions, ask when ambiguity affects behavior |
| Simplicity first | Prefer the smallest implementation that solves the stated problem |
| Surgical changes | Touch only required files and avoid drive-by cleanup |
| Goal-driven execution | Define success criteria and verify against them before reporting completion |

## Anti-Patterns To Catch

- Picking one interpretation silently when product behavior is ambiguous.
- Adding configurability, framework structure, or abstractions before a repeated need exists.
- Reformatting, rewriting comments, or "improving" adjacent code outside the request.
- Fixing a bug without a repro, root cause, or regression signal.
- Reporting success because code looks plausible rather than because the relevant path was verified.

## How To Use This Reference

Use this file to explain why the skill exists, not as a second workflow. The operational workflow lives in `SKILL.md`.
