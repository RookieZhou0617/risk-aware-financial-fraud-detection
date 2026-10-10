"""Offline presentation consistency checks; no research data or inference."""

import hashlib
import json
from pathlib import Path
import re
import statistics
import struct
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


class PublicEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "docs/evidence.json").read_text(encoding="utf-8"))

    def test_bilingual_headline_tables_match_aggregate_json(self):
        fields = ["auc_pr", "auc_roc", "fraud_f1_at_0_5",
                  "recall_at_5_percent", "recall_at_10_percent"]
        lightgbm = self.data["baselines"]["lightgbm"]["metrics"]
        lightgbm = {**lightgbm, "fraud_f1_at_0_5": lightgbm["f1_at_0_5"]}
        for filename in ("README.md", "README_CN.md"):
            content = (ROOT / filename).read_text(encoding="utf-8")
            for label, metrics in [("LightGBM", lightgbm)] + list(self.data["models"].items())[:2]:
                row = next(line for line in content.splitlines() if line.startswith(f"| {label} ·"))
                values = [cell.strip().replace("**", "") for cell in row.split("|")[2:-1]]
                self.assertEqual(values, [f"{metrics[field]:.6f}" for field in fields])

    def test_development_tables_match_aggregate_json(self):
        content = (ROOT / "docs/experiments.md").read_text(encoding="utf-8")
        controls = self.data["anchor_controls"]
        variants = self.data["relation_variants"]
        rows = {
            "No-deviation control": controls["no_deviation"]["years"],
            "Current-state-reference control": controls["current_state_reference"]["years"],
            "Shuffled-history control": controls["shuffled_history"]["years"],
            "MDRA · real company history": controls["real_company_history"]["years"],
            "Anchor-conditioned neighbor attention": variants["anchor_conditioned_neighbor_attention"]["years"],
            "Explicit difference representation": variants["explicit_difference_representation"]["years"],
        }
        for label, years in rows.items():
            row = next(line for line in content.splitlines() if line.startswith(f"| {label} |"))
            values = [cell.strip().replace("**", "") for cell in row.split("|")[2:7]]
            ordered = [years[str(year)] for year in range(2018, 2022)]
            self.assertEqual(values, [f"{value:.4f}" for value in ordered + [statistics.mean(ordered)]])
        for row in self.data["development"]:
            self.assertAlmostEqual(row["delta"], row["msar_hgrn"] - row["mdra"])
        self.assertLess(next(row["delta"] for row in self.data["development"] if row["year"] == 2019), 0)

    def test_uncertainty_and_comparison_boundaries_remain_present(self):
        for key in ("delta_anchor", "delta_relation"):
            low, high = self.data["bootstrap"][key]["ci95"]
            self.assertLess(low, 0)
            self.assertGreater(high, 0)
        self.assertEqual(self.data["source65_development"]["final_2022_status"], "BLOCKED_INPUT_UNAVAILABLE")
        self.assertEqual(set(self.data["source65_development"]["years"]), {"2018", "2019", "2020", "2021"})
        for name, row in self.data["literature_reports"].items():
            if name == "scope":
                continue
            self.assertTrue(row["source"].startswith("https://"))
            self.assertIn("setting", row)
            self.assertNotIn("fraud_f1_at_0_5", row)
        content = (ROOT / "docs/experiments.md").read_text(encoding="utf-8")
        self.assertIn("## Supplementary evidence", content)
        self.assertIn("Both intervals cross zero", content)
        self.assertIn("300 steps for real relations and 20", content)

    def test_local_markdown_targets_exist(self):
        for path in [ROOT / "README.md", ROOT / "README_CN.md", *sorted((ROOT / "docs").glob("*.md")), ROOT / "assets/README.md"]:
            content = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if re.match(r"(?:https?://|#)", target):
                    continue
                self.assertTrue((path.parent / target.split("#", 1)[0]).exists(), f"{path.name}: {target}")

    def test_public_presentation_is_experiment_focused(self):
        paths = [ROOT / "README.md", ROOT / "README_CN.md",
                 *sorted((ROOT / "docs").glob("*.md")), ROOT / "docs/evidence.json",
                 ROOT / "assets/README.md", ROOT / "assets/research-cover.svg",
                 ROOT / "scripts/render_assets.py", ROOT / "examples/README.md"]
        writing_metadata = re.compile(
            r"thes[i]s|manu[s]cript|master['’]s|chapter[ _0-9]|毕业论文|硕士|学位|写作进",
            re.IGNORECASE,
        )
        for path in paths:
            self.assertIsNone(writing_metadata.search(path.read_text(encoding="utf-8")), path.name)
        self.assertTrue((ROOT / "docs/experiment_status.md").exists())

    def test_figure_dimensions_checksum_and_svg_validity(self):
        png = (ROOT / "assets/model-framework.png").read_bytes()
        self.assertEqual(struct.unpack(">II", png[16:24]), (3000, 2187))
        manifest = (ROOT / "assets/README.md").read_text(encoding="utf-8")
        self.assertIn(hashlib.sha256(png).hexdigest(), manifest)
        for path in (ROOT / "assets").glob("*.svg"):
            self.assertEqual(ET.parse(path).getroot().tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
