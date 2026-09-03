---
name: test-driven-development
description: Applies a red-green-refactor cycle to behavior changes so tests prove the change before implementation. Use when the user requests TDD or test-first development, or when an implementation plan explicitly requires a failing regression test before feature or bug-fix code.
---

# Test-Driven Development

Use a failing behavioral test to define the change, then write the smallest implementation that makes it pass.

## Scope

Apply strict TDD when the user or approved plan requires it. For legacy code, generated artifacts, prototypes, or non-executable configuration where test-first is impractical, state the limitation and choose the closest reproducible verification rather than pretending a test failed first.

## Red-Green-Refactor Workflow

1. **Define one behavior**
   - Name the observable input, output, side effect, or failure.
   - Identify the production change that would make this test fail.

2. **RED: write the smallest test**
   - Exercise real production behavior; use mocks only at unavoidable external boundaries.
   - Keep one reason to fail per test.

3. **Verify RED**
   - Run the focused test and capture the expected failure.
   - A passing test means it does not prove the missing behavior. A setup error is not a valid red state.

4. **GREEN: implement minimally**
   - Add only enough production code to satisfy the current behavior.
   - Do not add speculative options, abstractions, or unrelated cleanup.

5. **Verify GREEN**
   - Run the focused test, then the nearest relevant suite.
   - Fix production code when the behavior is wrong; change the test only when the requirement or test itself was wrong.

6. **REFACTOR while green**
   - Improve names, duplication, and structure without changing behavior.
   - Rerun tests after refactoring.

7. **Repeat for the next behavior**

## Test Quality

Read [references/writing-good-tests.md](references/writing-good-tests.md) when creating or substantially changing tests. Prefer behavior assertions over implementation-detail assertions, deterministic signals over sleeps, and compact fixtures over production-only test hooks.

## Verification

- [ ] Each new behavior has a focused test.
- [ ] The test was observed failing for the expected reason before implementation.
- [ ] The minimal implementation made it pass.
- [ ] Refactoring occurred only while green.
- [ ] Relevant surrounding tests pass and output contains no unexplained failures or warnings.
