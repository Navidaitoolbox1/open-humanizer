"""Core analysis engine for the local Humanizer tool."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_rules(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _evidence(text: str) -> dict[str, list[str]]:
    dates = re.findall(r"\b(?:\d{1,2} [A-Z][a-z]+ \d{4}|\d{4}-\d{2}-\d{2})\b", text)
    numbers = re.findall(r"(?<![\w-])\d+(?:\.\d+)?%?\b", text)
    return {"dates": list(dict.fromkeys(dates)), "numbers": list(dict.fromkeys(numbers))}


def analyze_text(text: str, rules: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for rule in rules.get("rules", []):
        for pattern in rule.get("patterns", []):
            flags = re.IGNORECASE if pattern != "—" else 0
            for match in re.finditer(re.escape(pattern), text, flags):
                findings.append({
                    "rule_id": rule["id"],
                    "label": rule["label"],
                    "severity": rule["severity"],
                    "match": match.group(0),
                    "line": _line_number(text, match.start()),
                    "suggestion": rule["suggestion"],
                })
    findings.sort(key=lambda item: (item["line"], item["match"].lower()))
    counts = {level: sum(f["severity"] == level for f in findings) for level in ("high", "medium", "low")}
    penalty = counts["high"] * 12 + counts["medium"] * 6 + counts["low"] * 2
    score = max(0, 100 - penalty)
    return {
        "tool": "open-humanizer",
        "version": rules.get("version", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"finding_count": len(findings), "severity_counts": counts, "editorial_score": score, "status": "review" if findings else "clear"},
        "evidence": _evidence(text),
        "findings": findings,
        "disclaimer": "This is an editorial quality check, not an AI detector and not a guarantee of human authorship.",
    }
