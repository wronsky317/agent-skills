#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"
load_agent_targets

echo "root: $ROOT"
echo "config: $CONFIG_FILE"
echo "skills root: $SKILLS_ROOT"
echo "managed skills:"
find "$SKILLS_ROOT" -type f -name SKILL.md -not -path '*/.git/*' -print | sed 's#/SKILL.md$##' | sort

echo
echo "agent targets:"
for i in "${!AGENT_TARGETS[@]}"; do
  agent="${AGENT_NAMES[$i]}"
  target="${AGENT_TARGETS[$i]}"
  if [[ -L "$target" ]]; then
    echo "$agent: symlink target: $target -> $(readlink "$target")"
  elif [[ -d "$target" ]]; then
    count="$(find "$target" -maxdepth 1 -type l | wc -l | tr -d ' ')"
    echo "$agent: directory target: $target ($count symlinks)"
    if [[ -L "$target/.system" ]]; then
      echo "  system link: $target/.system -> $(readlink "$target/.system")"
    fi
  else
    echo "$agent: missing target: $target"
  fi
done
