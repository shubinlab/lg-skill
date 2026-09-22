from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = {
    "README.md": ["Why install it?", "Compatibility at a glance", "What it can do", "What it cannot promise", "Quick start", "Contributing", "License"],
    "SKILL.md": ["name: lg-monitor-control", "Safety and scope", "Verification"],
    "CONTRIBUTING.md": ["Development loop"],
    "SECURITY.md": ["Do not publish"],
    "docs/compatibility.md": ["Support tiers", "Transport matrix", "Not promised"],
}

for filename, needles in required.items():
    text = (ROOT / filename).read_text(encoding="utf-8")
    for needle in needles:
        assert needle in text, f"{filename}: missing {needle!r}"
    assert not re.search(r"gho_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+", text), f"{filename}: token-like secret"

for svg in (ROOT / "assets").glob("*.svg"):
    ET.parse(svg)

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for asset in ("assets/hero-monitor.svg", "assets/control-flow.svg", "assets/evidence-card.svg"):
    assert asset in readme, f"README.md: missing asset link {asset}"
assert "docs/compatibility.md" in readme, "README.md: missing compatibility matrix link"

print("skill repository validation: ok")
