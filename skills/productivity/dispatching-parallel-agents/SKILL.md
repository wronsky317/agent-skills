---
name: dispatching-parallel-agents
description: Coordinates two or more independent subtasks through parallel agents with focused prompts and explicit integration checks. Use when the user asks for delegation or parallel agent work, or when an active orchestration workflow explicitly permits subagents and the tasks do not share mutable state or sequential dependencies.
---

# Dispatching Parallel Agents

Use parallel agents to reduce latency without fragmenting ownership or allowing concurrent edits to collide.

## Decision Gate

Delegate only when both are true:

1. Subagents are authorized by the user, system instructions, or an already-active orchestration skill.
2. At least two tasks can be completed independently.

Do not delegate when tasks share files, depend on the same evolving state, require one root-cause investigation, or would need the full conversation to make sound decisions.

## Workflow

1. **Partition by outcome**
   - Give each agent one bounded problem domain and a clear finish condition.
   - Prefer read-only analysis in parallel when edit ownership would overlap.

2. **Assign ownership**
   - Name exact files or subsystems each agent may edit.
   - State shared-workspace constraints; agents may see one another's changes.
   - Reserve integration, cross-cutting edits, and final verification for the coordinator.

3. **Write self-contained prompts**
   - Include the goal, relevant paths, known evidence, constraints, verification command, and expected report.
   - Pass only the context needed for that subtask.
   - Tell agents not to undo unrelated or concurrent changes.

4. **Dispatch concurrently**
   - Start all independent tasks before waiting.
   - Keep one slot available for coordinator work when the environment has limited concurrency.

5. **Integrate deliberately**
   - Read every report and inspect the actual filesystem or diff.
   - Resolve overlapping edits explicitly.
   - Run combined verification after individual checks pass.

## Prompt Template

```markdown
Goal: [one bounded outcome]
Scope: [files/subsystem]
Evidence: [errors, requirements, or relevant context]
Constraints: [what must not change; shared-workspace warning]
Verify: [specific command or artifact]
Return: [root cause or changes, tests, risks, files touched]
```

## Verification

- [ ] Delegation was authorized.
- [ ] Tasks were independent and edit ownership did not overlap.
- [ ] Agent claims were checked against files, diffs, or command output.
- [ ] Integrated behavior was verified after all results were combined.
- [ ] Residual conflicts or unverified paths were reported.
