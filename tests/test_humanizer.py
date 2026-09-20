import json
import unittest
from pathlib import Path

from humanizer.engine import analyze_text, load_rules


class HumanizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(Path(__file__).parents[1] / "rules" / "writing_rules.json")

    def test_flags_promotional_phrase_and_vague_attribution(self):
        text = "This groundbreaking solution offers a seamless experience. Experts say it is widely recognised."
        report = analyze_text(text, self.rules)
        rule_ids = {finding["rule_id"] for finding in report["findings"]}
        self.assertIn("promotional_language", rule_ids)
        self.assertIn("vague_attribution", rule_ids)
        self.assertGreater(report["summary"]["finding_count"], 0)

    def test_flags_em_dash_placeholder_and_internal_marker(self):
        text = "The result — [DATE] contentReference shows the next step."
        report = analyze_text(text, self.rules)
        rule_ids = {finding["rule_id"] for finding in report["findings"]}
        self.assertIn("em_dash", rule_ids)
        self.assertIn("placeholder", rule_ids)
        self.assertIn("internal_marker", rule_ids)

    def test_clean_text_has_no_findings_and_keeps_evidence(self):
        text = "On 12 September 2026, the audit recorded 5 clicks from Search Console. The next review is scheduled for 19 September 2026."
        report = analyze_text(text, self.rules)
        self.assertEqual(report["summary"]["finding_count"], 0)
        self.assertIn("12 September 2026", report["evidence"]["dates"])
        self.assertIn("5", report["evidence"]["numbers"])

    def test_output_is_json_serialisable(self):
        report = analyze_text("The report shows a pending decision.", self.rules)
        json.dumps(report)


if __name__ == "__main__":
    unittest.main()
