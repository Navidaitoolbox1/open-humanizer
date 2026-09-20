"""Command-line interface for Open Humanizer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import analyze_text, load_rules


def main() -> int:
    parser = argparse.ArgumentParser(description="Local editorial quality checker for natural English writing.")
    parser.add_argument("input", nargs="?", help="Text file to analyze. Reads stdin when omitted.")
    parser.add_argument("--rules", default=str(Path(__file__).parents[1] / "rules" / "writing_rules.json"))
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()
    text = Path(args.input).read_text(encoding="utf-8") if args.input else __import__("sys").stdin.read()
    report = analyze_text(text, load_rules(Path(args.rules)))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        summary = report["summary"]
        print(f"Status: {summary['status']} | Editorial score: {summary['editorial_score']}/100")
        print(f"Findings: {summary['finding_count']} (high={summary['severity_counts']['high']}, medium={summary['severity_counts']['medium']}, low={summary['severity_counts']['low']})")
        for item in report["findings"]:
            print(f"L{item['line']} [{item['severity']}] {item['label']}: {item['match']}\n  {item['suggestion']}")
        print("\nThis is an editorial quality check, not an AI detector.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
