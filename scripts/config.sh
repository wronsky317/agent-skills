#!/usr/bin/env bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$script_dir/.." && pwd)"
SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$ROOT/skills}"
SYSTEM_DIR="${AGENT_SKILLS_SYSTEM_DIR:-$ROOT/.system}"
CONFIG_FILE="${AGENT_SKILLS_CONFIG:-$ROOT/config/agents.conf}"
CONFIG_EXAMPLE="$ROOT/config/agents.conf.example"

load_agent_targets() {
  AGENT_NAMES=()
  AGENT_TARGETS=()

  if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "missing local config file: $CONFIG_FILE" >&2
    if [[ -f "$CONFIG_EXAMPLE" ]]; then
      echo "create it from the template:" >&2
      echo "  cp \"$CONFIG_EXAMPLE\" \"$CONFIG_FILE\"" >&2
    fi
    exit 1
  fi

  local line agent target
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    [[ -z "$line" || "${line:0:1}" == "#" ]] && continue

    if [[ "$line" != *"|"* ]]; then
      echo "invalid config line, expected agent|path: $line" >&2
      exit 1
    fi

    agent="${line%%|*}"
    target="${line#*|}"
    agent="${agent#"${agent%%[![:space:]]*}"}"
    agent="${agent%"${agent##*[![:space:]]}"}"
    target="${target#"${target%%[![:space:]]*}"}"
    target="${target%"${target##*[![:space:]]}"}"

    if [[ ! "$agent" =~ ^[A-Za-z0-9_-]+$ ]]; then
      echo "invalid agent name in config: $agent" >&2
      exit 1
    fi

    case "$target" in
      "~") target="$HOME" ;;
      "~/"*) target="$HOME/${target#~/}" ;;
    esac

    target="$(eval "printf '%s' \"$target\"")"

    AGENT_NAMES+=("$agent")
    AGENT_TARGETS+=("$target")
  done < "$CONFIG_FILE"

  if [[ "${#AGENT_TARGETS[@]}" -eq 0 ]]; then
    echo "no agent targets configured in: $CONFIG_FILE" >&2
    exit 1
  fi
}
