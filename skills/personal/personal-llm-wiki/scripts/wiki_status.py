#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("/Users/wronsky/Documents/Agent技能")
WIKI = ROOT / "wiki"


def print_file(path: Path, max_lines: int) -> None:
    print(f"\n## {path}")
    if not path.exists():
        print("missing")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    for line in lines[:max_lines]:
        print(line)
    if len(lines) > max_lines:
        print(f"... ({len(lines) - max_lines} more lines)")


def main() -> int:
    print(f"wiki_root: {ROOT}")
    print(f"agents: {ROOT / 'AGENTS.md'}")
    print(f"index: {WIKI / 'index.md'}")
    print(f"log: {WIKI / 'log.md'}")

    print("\n## Files")
    if WIKI.exists():
        for path in sorted(WIKI.rglob("*.md")):
            print(path.relative_to(ROOT))
    else:
        print("wiki directory missing")

    print_file(WIKI / "index.md", 80)

    log = WIKI / "log.md"
    print(f"\n## Recent log entries from {log}")
    if log.exists():
        entries = [line for line in log.read_text(encoding="utf-8").splitlines()
                   if line.startswith("## [")]
        for line in entries[-10:]:
            print(line)
    else:
        print("missing")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
