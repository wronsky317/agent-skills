#!/usr/bin/env python3
"""Validate shared agent skills.

Hard errors block repository hygiene:
- missing/malformed frontmatter
- missing name or description
- skill name not matching directory name
- overlong descriptions

Warnings identify cleanup work without breaking existing historical skills.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
MAX_DESCRIPTION_CHARS = 1024
LONG_SKILL_LINES = 500

PROCESS_HEADINGS = (
    "workflow",
    "process",
    "procedure",
    "steps",
    "instructions",
    "how to use",
    "review order",
    "核心职责",
    "工作流程",
)

VERIFICATION_HEADINGS = (
    "verification",
    "validate",
    "validation",
    "quality bar",
    "checklist",
    "验证",
    "验收",
)

TRIGGER_MARKERS = (
    "use when",
    "when ",
    "当用户",
    "触发",
    "使用场景",
    "适用于",
)

SKILL_REF_PATTERNS = (
    re.compile(r"`([a-z][a-z0-9-]+[a-z0-9])`\s+skill\b"),
    re.compile(r"\b(?:use|follow|invoke)\s+(?:the\s+)?`([a-z][a-z0-9-]+[a-z0-9])`\s+skill\b"),
    re.compile(r"\bskills/[a-z0-9-]+/([a-z][a-z0-9-]+[a-z0-9])/SKILL\.md\b"),
)


@dataclass
class Result:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    match = re.match(r"^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n", text)
    if not match:
        return None, text

    frontmatter: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            frontmatter[key] = value

    return frontmatter, text[match.end() :]


def heading_lines(body: str) -> list[str]:
    headings: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip().lower())
    return headings


def has_heading(headings: list[str], markers: tuple[str, ...]) -> bool:
    return any(any(marker in heading for marker in markers) for heading in headings)


def extract_skill_refs(text: str) -> set[str]:
    refs: set[str] = set()
    for pattern in SKILL_REF_PATTERNS:
        refs.update(pattern.findall(text))
    return refs


def validate_skill(path: Path, known_skills: set[str]) -> Result:
    result = Result(path=path)
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    skill_name = path.parent.name

    if frontmatter is None:
        result.errors.append("missing or malformed YAML frontmatter")
        return result

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        result.errors.append("frontmatter missing required field: name")
    elif name != skill_name:
        result.errors.append(f"frontmatter name '{name}' does not match directory '{skill_name}'")

    if not description:
        result.errors.append("frontmatter missing required field: description")
    else:
        if len(description) > MAX_DESCRIPTION_CHARS:
            result.errors.append(
                f"description is {len(description)} characters; max is {MAX_DESCRIPTION_CHARS}"
            )
        lowered_description = description.lower()
        if not any(marker in lowered_description for marker in TRIGGER_MARKERS):
            result.warnings.append("description may not include clear trigger language")
        if len(description) < 40:
            result.warnings.append("description is very short; discovery may be weak")

    line_count = len(text.splitlines())
    if line_count > LONG_SKILL_LINES:
        result.warnings.append(f"SKILL.md is {line_count} lines; consider progressive disclosure")

    headings = heading_lines(body)
    if not has_heading(headings, PROCESS_HEADINGS):
        result.warnings.append("no obvious workflow/process/instructions heading found")
    if not has_heading(headings, VERIFICATION_HEADINGS):
        result.warnings.append("no obvious verification/checklist/quality heading found")

    for ref in sorted(extract_skill_refs(text)):
        if ref not in known_skills:
            result.warnings.append(f"possible dead skill reference: {ref}")

    return result


def main() -> int:
    if not SKILLS_ROOT.exists():
        print(f"ERROR: skills root not found: {SKILLS_ROOT}", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    known_skills = {path.parent.name for path in skill_files}

    total_errors = 0
    total_warnings = 0

    for path in skill_files:
        result = validate_skill(path, known_skills)
        rel = path.relative_to(REPO_ROOT)
        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

        if not result.errors and not result.warnings:
            print(f"OK    {rel}")
            continue

        status = "FAIL" if result.errors else "WARN"
        print(f"{status}  {rel}")
        for message in result.errors:
            print(f"      ERROR: {message}")
        for message in result.warnings:
            print(f"      WARN:  {message}")

    print()
    print(
        f"{len(skill_files)} skills checked; "
        f"{total_errors} error(s), {total_warnings} warning(s)"
    )

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
