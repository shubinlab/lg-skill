from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = {
    "README.md": ["Quick start", "Safe baseline", "Control map", "Contributing", "License"],
    "SKILL.md": ["name: lg-monitor-control", "Safety and scope", "Verification"],
    "CONTRIBUTING.md": ["Development loop"],
    "SECURITY.md": ["Do not publish"],
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

print("skill repository validation: ok")
