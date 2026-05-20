#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"
load_agent_targets

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
