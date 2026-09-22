# Agent compatibility and installation

The repository uses the open `SKILL.md` format: one skill directory, one `SKILL.md`, YAML frontmatter with `name` and `description`, and optional `scripts/`, `references/`, and `assets/`.

## Universal install — recommended

The interoperable path works for Codex, VS Code/Copilot, Cursor, Gemini CLI, Cline, OpenCode, and other Agent Skills clients:

### Project scope

```bash
mkdir -p .agents/skills/lg-monitor-control
cp SKILL.md .agents/skills/lg-monitor-control/SKILL.md
```

### User scope

```bash
mkdir -p ~/.agents/skills/lg-monitor-control
cp SKILL.md ~/.agents/skills/lg-monitor-control/SKILL.md
```

The project path keeps the skill with a repository. The user path makes it available across repositories.

## Client matrix

| Agent/client | Project path | User path | Reload/check |
| --- | --- | --- | --- |
| **OpenAI Codex** | `.agents/skills/lg-monitor-control/` | `~/.agents/skills/lg-monitor-control/` | `/skills` or invoke `$lg-monitor-control` |
| **VS Code / GitHub Copilot** | `.agents/skills/` or `.github/skills/` | `~/.agents/skills/` or `~/.copilot/skills/` | `/skills list`, `/skills reload` |
| **Cursor** | `.cursor/skills/lg-monitor-control/` | `~/.cursor/skills/lg-monitor-control/` | Settings → Skills; reload Cursor |
| **Claude Code** | `.claude/skills/lg-monitor-control/` | `~/.claude/skills/lg-monitor-control/` | `/skills`, then `/lg-monitor-control` |
| **Gemini CLI** | `.gemini/skills/lg-monitor-control/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | `/skills list`, `/skills reload` |
| **OpenCode** | `.opencode/skills/lg-monitor-control/` or `.agents/skills/` | `~/.config/opencode/skills/` | restart or inspect the skill list |
| **Roo Code** | `.roo/skills/lg-monitor-control/` or `.agents/skills/` | `~/.roo/skills/` | automatic discovery; reload extension |
| **Cline** | `.cline/skills/lg-monitor-control/` or `.agents/skills/` | `~/.cline/skills/` | reload skills in Cline |
| **Windsurf Cascade** | `.devin/skills/lg-monitor-control/` or legacy `.windsurf/skills/` | `~/.codeium/windsurf/skills/` | restart/reload Cascade |

When a client supports `.agents/skills`, use that path first. Client-native paths are included for clients that do not scan the shared directory in the installed version.

## Install from GitHub

```bash
git clone --depth 1 https://github.com/shubinlab/lg-skill.git
cd lg-skill

# Universal project install
mkdir -p ../your-project/.agents/skills/lg-monitor-control
cp SKILL.md ../your-project/.agents/skills/lg-monitor-control/SKILL.md
```

If your client has a native installer, use it after reviewing `SKILL.md`. A skill is executable guidance: inspect scripts and permissions before granting tool access.

## Agent-specific examples

### Codex / Agent Skills compatible clients

```bash
mkdir -p ~/.agents/skills/lg-monitor-control
cp SKILL.md ~/.agents/skills/lg-monitor-control/SKILL.md
```

### Claude Code

```bash
mkdir -p ~/.claude/skills/lg-monitor-control
cp SKILL.md ~/.claude/skills/lg-monitor-control/SKILL.md
```

### Gemini CLI

```bash
gemini skills install https://github.com/shubinlab/lg-skill.git
# or, for a project-only install:
gemini skills install https://github.com/shubinlab/lg-skill.git --scope workspace
```

### OpenCode

```bash
mkdir -p ~/.config/opencode/skills/lg-monitor-control
cp SKILL.md ~/.config/opencode/skills/lg-monitor-control/SKILL.md
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills\lg-monitor-control"
Copy-Item .\SKILL.md "$HOME\.agents\skills\lg-monitor-control\SKILL.md"
```

## Agent safety

The skill describes platform adapters but does not grant an agent permissions. The agent still needs access to `ddcutil`, `modetest`, `hyprctl`, or the Windows/macOS monitor tool used by the platform adapter. Review commands before allowing writes.

## Official references

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Codex skills](https://developers.openai.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor skills](https://cursor.com/docs/skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [GitHub Copilot agent skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [OpenCode skills](https://opencode.ai/docs/skills)
- [Roo Code skills](https://roocodeinc.github.io/Roo-Code/features/skills/)
- [Cline skills](https://docs.cline.bot/customization/skills)
- [Windsurf Cascade skills](https://docs.windsurf.com/windsurf/cascade/skills)
