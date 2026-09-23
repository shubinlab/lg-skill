from pathlib import Path
import re
import stat
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = {
    "README.md": ["Why install it?", "Compatibility at a glance", "Use it with your agent", "Operating systems", "What it can do", "What it cannot promise", "Quick start", "Contributing", "License"],
    "SKILL.md": ["name: lg-monitor-control", "Agent and platform adapters", "Safety and scope", "Verification"],
    "CONTRIBUTING.md": ["Development loop"],
    "SECURITY.md": ["Do not publish"],
    "docs/compatibility.md": ["Support tiers", "Transport matrix", "Not promised"],
    "docs/agents.md": ["Universal install", "Client matrix", "OpenAI Codex", "Windsurf Cascade"],
    "docs/platforms.md": ["OS matrix", "Linux adapter", "Windows adapter", "Universal limits"],
}

for filename, needles in required.items():
    text = (ROOT / filename).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{filename}: missing {needle!r}"
    assert not re.search(r"gho_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+", text), f"{filename}: token-like secret"

for svg in (ROOT / "assets").glob("*.svg"):
    ET.parse(svg)

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for asset in ("assets/hero-monitor.svg", "assets/control-flow.svg", "assets/evidence-card.svg", "assets/compatibility-map.svg"):
    assert asset in readme, f"README.md: missing asset link {asset}"
for doc in ("docs/compatibility.md", "docs/agents.md", "docs/platforms.md"):
    assert doc in readme or doc in (ROOT / "docs/compatibility.md").read_text(encoding="utf-8"), f"missing documentation reference {doc}"

for script in (ROOT / "scripts/install-skill.sh",):
    assert script.stat().st_mode & stat.S_IXUSR, f"{script}: must be executable"

print("skill repository validation: ok")
