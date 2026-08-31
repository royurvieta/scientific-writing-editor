#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "scientific-writing-editor"


def load_checker():
    path = SKILL / "scripts" / "check_fidelity.py"
    spec = importlib.util.spec_from_file_location("check_fidelity", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_builder():
    path = ROOT / "scripts" / "build_packages.py"
    spec = importlib.util.spec_from_file_location("build_packages", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicSkillContractTests(unittest.TestCase):
    def test_skill_has_public_name_and_three_modes(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^name: scientific-writing-editor$")
        self.assertIn("### REWRITE", text)
        self.assertIn("### REVIEWER RESPONSE", text)
        self.assertIn("### DETECT", text)

    def test_public_files_do_not_brand_the_skill_as_roy(self) -> None:
        checked = [
            ROOT / "README.md",
            SKILL / "SKILL.md",
            SKILL / "agents" / "openai.yaml",
            *sorted((SKILL / "references").glob("*.md")),
        ]
        for path in checked:
            self.assertNotRegex(path.read_text(encoding="utf-8"), r"(?i)\broy\b", path)

    def test_repo_has_public_distribution_files(self) -> None:
        required = [
            ROOT / "README.md",
            ROOT / "LICENSE",
            ROOT / "THIRD_PARTY_NOTICES.md",
            ROOT / ".github" / "workflows" / "ci.yml",
            ROOT / "scripts" / "build_packages.py",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)

    def test_skill_links_all_runtime_references(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for name in [
            "anti-slop-bilingual.md",
            "evaluation.md",
            "examples.md",
            "personal-voice.md",
            "reviewer-responses.md",
        ]:
            self.assertIn(f"references/{name}", text)
            self.assertTrue((SKILL / "references" / name).is_file())

    def test_public_material_contains_no_private_research_fixtures(self) -> None:
        private_markers = re.compile(
            r"(?i)(?:\btan" r"nin\b|astring" r"en|\bdav" r"is\b|red[- ]wi" r"ne|"
            r"\bwi" r"nes?\b|\bvi" r"nos?\b|473 of 1," r"400|city li" r"ft|per-wi" r"ne lift|"
            r"/Us" r"ers/|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,})"
        )
        for path in ROOT.rglob("*"):
            if (
                not path.is_file()
                or ".git" in path.parts
                or "dist" in path.parts
                or "__pycache__" in path.parts
            ):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            self.assertNotRegex(text, private_markers, path)

    def test_no_scaffold_placeholders_remain(self) -> None:
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts and "tests" not in path.parts:
                text = path.read_text(encoding="utf-8", errors="ignore")
                self.assertNotRegex(text, r"\b(?:TODO|TBD|PLACEHOLDER)\b", path)


class FidelityCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_checker()

    def test_literal_inventory_accepts_reordering(self) -> None:
        source = "The mean fell by 12% after 6 months (p = 0.18; 95% CI: -2.1 to 0.4 mg/L)."
        rewrite = "After 6 months, the mean fell by 12% (p = 0.18; 95% CI: -2.1 to 0.4 mg/L)."
        self.assertEqual({}, self.checker.compare(source, rewrite))

    def test_literal_inventory_rejects_changed_number(self) -> None:
        mismatch = self.checker.compare("n = 140; p = 0.08", "n = 104; p = 0.08")
        self.assertEqual({"140": 1}, mismatch["numbers"]["missing_from_rewrite"])
        self.assertEqual({"104": 1}, mismatch["numbers"]["added_in_rewrite"])

    def test_binding_check_flags_swapped_values(self) -> None:
        source = "Site North had an index of 1.46; Site South had an index of 1.18."
        rewrite = "Site North had an index of 1.18; Site South had an index of 1.46."
        changes = self.checker.binding_changes(source, rewrite)
        self.assertEqual({"1.46", "1.18"}, {item["marker"] for item in changes})

    def test_quote_check_flags_changed_exact_wording(self) -> None:
        source = 'Caption added: "Selected by enrichment, not frequency."'
        rewrite = 'Caption added: "Selected by frequency, not enrichment."'
        mismatch = self.checker.quote_mismatches(source, rewrite)
        self.assertTrue(mismatch["changed"])


class PackageBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.builder = load_builder()

    def test_archive_has_single_top_level_skill_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_zip = self.builder.build_packages(Path(directory))
            self.assertEqual("scientific-writing-editor.zip", skill_zip.name)

            with zipfile.ZipFile(skill_zip) as archive:
                names = archive.namelist()
                self.assertIn("scientific-writing-editor/SKILL.md", names)
                top_level = {name.split("/", 1)[0] for name in names}
                self.assertEqual({"scientific-writing-editor"}, top_level)
                for name in names:
                    self.assertIn("/", name, f"file at archive root: {name}")
                    self.assertTrue(
                        name.startswith("scientific-writing-editor/"), name
                    )
                self.assertTrue(all("__pycache__" not in name and "/._" not in name for name in names))


if __name__ == "__main__":
    unittest.main(verbosity=2)
