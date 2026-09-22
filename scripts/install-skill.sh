#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-skill.sh [--scope project|user] [--agent agents|claude|cursor|gemini|copilot|opencode|roo|cline|windsurf]

Defaults: --scope user --agent agents
EOF
}

scope=user
agent=agents
while (($#)); do
  case "$1" in
    --scope) scope=${2:?missing scope}; shift 2 ;;
    --agent) agent=${2:?missing agent}; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$agent" in
  agents) user_root="$HOME/.agents/skills"; project_root=".agents/skills" ;;
  claude) user_root="$HOME/.claude/skills"; project_root=".claude/skills" ;;
  cursor) user_root="$HOME/.cursor/skills"; project_root=".cursor/skills" ;;
  gemini) user_root="$HOME/.gemini/skills"; project_root=".gemini/skills" ;;
  copilot) user_root="$HOME/.copilot/skills"; project_root=".github/skills" ;;
  opencode) user_root="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills"; project_root=".opencode/skills" ;;
  roo) user_root="$HOME/.roo/skills"; project_root=".roo/skills" ;;
  cline) user_root="$HOME/.cline/skills"; project_root=".cline/skills" ;;
  windsurf) user_root="$HOME/.codeium/windsurf/skills"; project_root=".devin/skills" ;;
  *) echo "unsupported agent adapter: $agent" >&2; exit 2 ;;
esac

if [[ "$scope" == user ]]; then
  destination="$user_root/lg-monitor-control"
elif [[ "$scope" == project ]]; then
  destination="$project_root/lg-monitor-control"
else
  echo "unsupported scope: $scope" >&2
  exit 2
fi

mkdir -p "$destination"
cp SKILL.md "$destination/SKILL.md"
printf 'installed lg-monitor-control -> %s\n' "$destination"
