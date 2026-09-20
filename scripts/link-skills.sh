#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"
load_agent_targets

# Record existing Codex homes before linking creates any target directories.
CODEX_HOMES=()
for i in "${!AGENT_NAMES[@]}"; do
  [[ "${AGENT_NAMES[$i]}" == "codex" ]] || continue
  codex_home="$(dirname "${AGENT_TARGETS[$i]%/}")"
  if [[ -d "$codex_home" ]]; then
    CODEX_HOMES+=("$codex_home")
  else
    echo "skip Codex routing: Codex home does not exist: $codex_home"
  fi
done

tmp="$(mktemp)"
trap 'rm -f "$tmp" "$tmp.names" "$tmp.dupes"' EXIT

find "$SKILLS_ROOT" -type f -name SKILL.md -not -path '*/.git/*' -print | while IFS= read -r skill_file; do
  skill_dir="${skill_file%/SKILL.md}"
  skill_name="$(basename "$skill_dir")"
  printf '%s\t%s\n' "$skill_name" "$skill_dir"
done | sort > "$tmp"

cut -f1 "$tmp" | sort > "$tmp.names"
uniq -d "$tmp.names" > "$tmp.dupes"
if [[ -s "$tmp.dupes" ]]; then
  echo "duplicate skill names found; refusing to link:"
  cat "$tmp.dupes"
  exit 1
fi

for target in "${AGENT_TARGETS[@]}"; do
  mkdir -p "$target"
done

if [[ -d "$SYSTEM_DIR" ]]; then
  for target in "${AGENT_TARGETS[@]}"; do
    system_link="$target/.system"
    if [[ -L "$system_link" ]]; then
      ln -sfn "$SYSTEM_DIR" "$system_link"
      echo "updated: $system_link -> $SYSTEM_DIR"
    elif [[ -e "$system_link" ]]; then
      echo "skip existing non-symlink: $system_link"
    else
      ln -s "$SYSTEM_DIR" "$system_link"
      echo "created: $system_link -> $SYSTEM_DIR"
    fi
  done
fi

while IFS=$'\t' read -r skill_name skill_dir; do
  [[ -n "$skill_name" ]] || continue
  for target in "${AGENT_TARGETS[@]}"; do
    link_path="$target/$skill_name"
    if [[ -L "$link_path" ]]; then
      ln -sfn "$skill_dir" "$link_path"
      echo "updated: $link_path -> $skill_dir"
    elif [[ -e "$link_path" ]]; then
      echo "skip existing non-symlink: $link_path"
    else
      ln -s "$skill_dir" "$link_path"
      echo "created: $link_path -> $skill_dir"
    fi
  done
done < "$tmp"

for codex_home in ${CODEX_HOMES[@]+"${CODEX_HOMES[@]}"}; do
  # Use the discovered source, never an unrelated pre-existing target skill.
  routing_dir=""
  while IFS=$'\t' read -r skill_name skill_dir; do
    if [[ "$skill_name" == "codex-subagent-routing" ]]; then
      routing_dir="$skill_dir"
      break
    fi
  done < "$tmp"
  if [[ -z "$routing_dir" ]]; then
    echo "skip Codex routing: codex-subagent-routing skill not found"
    continue
  fi
  if [[ ! -f "$routing_dir/scripts/manage.py" ]]; then
    echo "ERROR: Codex routing installer missing: $routing_dir/scripts/manage.py" >&2
    exit 1
  fi

  routing_python=""
  candidates=("${AGENT_SKILLS_PYTHON:-}" python3 python3.14 python3.13 python3.12 python3.11
    /opt/homebrew/bin/python3 /usr/local/bin/python3
    "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3")
  for candidate in "${candidates[@]}"; do
    [[ -n "$candidate" ]] || continue
    if "$candidate" -c 'import sys, tomllib; sys.exit(sys.version_info < (3, 11))' >/dev/null 2>&1; then
      routing_python="$candidate"
      break
    fi
  done
  if [[ -z "$routing_python" ]]; then
    echo "ERROR: Codex routing requires Python 3.11+; set AGENT_SKILLS_PYTHON to its executable." >&2
    exit 1
  fi

  echo "checking Codex routing: $codex_home (Python: $routing_python)"
  # The installer validates all role files and policy conflicts before writing.
  # apply is idempotent, preserves custom roles and backs up changed files.
  "$routing_python" "$routing_dir/scripts/manage.py" show --codex-home "$codex_home"
  "$routing_python" "$routing_dir/scripts/manage.py" apply --codex-home "$codex_home"
  "$routing_python" "$routing_dir/scripts/manage.py" check --codex-home "$codex_home"
done
