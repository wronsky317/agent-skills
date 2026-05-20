#!/usr/bin/env bash
set -euo pipefail

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"
load_agent_targets

INBOX="$SKILLS_ROOT/inbox"
LINK_SCRIPT="$ROOT/scripts/link-skills.sh"

mkdir -p "$INBOX"

for i in "${!AGENT_TARGETS[@]}"; do
  agent="${AGENT_NAMES[$i]}"
  target="${AGENT_TARGETS[$i]}"
  [[ -d "$target" ]] || continue
  for path in "$target"/*; do
    [[ -d "$path" ]] || continue
    [[ ! -L "$path" ]] || continue
    [[ -f "$path/SKILL.md" ]] || continue

    name="$(basename "$path")"
    dest="$INBOX/$agent/$name"
    if [[ -e "$dest" ]]; then
      stamp="$(date +%Y%m%d-%H%M%S)"
      dest="$INBOX/$agent/${name}-$stamp"
    fi
    mkdir -p "$(dirname "$dest")"
    mv "$path" "$dest"
    echo "imported: $path -> $dest"
  done
done

"$LINK_SCRIPT"
