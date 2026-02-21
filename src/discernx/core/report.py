from __future__ import annotations
from typing import Dict, Any


def to_markdown(data: Dict[str, Any]) -> str:
    overall = data.get("overall_risk", 0)
    md = []
    md.append("# Discern-X-Ray Report")
    md.append("")
    md.append(f"**Overall Risk Score:** {overall}/100")
    md.append("")
    md.append("## Claims")
    md.append("")
    claims = data.get("claims", [])
    if not claims:
        md.append("_No claims detected._")
    else:
        for c in claims:
            md.append(f"### Claim {c['id']} — Risk {c['risk_score']}/100")
            md.append(f"> {c['text']}")
            signals = c.get("signals", [])
            if signals:
                md.append("")
                md.append("Signals: " + ", ".join(f"`{s}`" for s in signals))
            md.append("")
    md.append("## Notes")
    for n in data.get("notes", []):
        md.append(f"- {n}")
    md.append("")
    return "\n".join(md)