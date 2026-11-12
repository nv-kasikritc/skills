#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Regression coverage for initial plugin versions and subsequent releases."""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "version-plugins.py"
SPEC = importlib.util.spec_from_file_location("version_plugins", SCRIPT)
vp = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = vp
SPEC.loader.exec_module(vp)


class TestPluginVersions(unittest.TestCase):
    def analysis(self, base, head):
        return vp.PluginAnalysis(
            name="sample",
            yaml_path=Path("plugins.d/sample.yml"),
            base_version=vp.SemVer.parse(base),
            head_version=vp.SemVer.parse(head),
            builder_changed_version=True,
            change_kind=vp.ChangeKind.STRUCTURAL,
        )

    def test_new_plugin_accepts_its_initial_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_yaml = root / "plugins.d/sample.yml"
            plugin_yaml.parent.mkdir()
            plugin_yaml.write_text('name: sample\nversion: "0.1.0"\n')
            with (
                mock.patch.object(vp, "REPO_ROOT", root),
                mock.patch.object(vp, "PLUGINS_DIR", root / "plugins"),
                mock.patch.object(vp, "PLUGINS_D_DEFAULTS", root / "plugins.d/_defaults.yml"),
                mock.patch.object(vp, "read_yaml_at_ref", return_value=None),
            ):
                analysis = vp.analyze_plugin(plugin_yaml, "base", root / "base")

            self.assertIsNone(analysis.base_version)
            self.assertEqual(analysis.change_kind, vp.ChangeKind.STRUCTURAL)
            self.assertEqual(vp.decide(analysis), ("accept", None))
            plan = vp.build_plan([analysis])
            self.assertEqual(plan.findings, [])
            self.assertEqual(plan.bumps, [])

    def test_existing_plugin_cannot_reuse_a_builder_set_version(self):
        verdict, reason = vp.decide(self.analysis("0.1.0", "0.1.0"))
        self.assertEqual(verdict, "fail")
        self.assertIn("version did not increase", reason)

    def test_existing_plugin_cannot_decrease_its_version(self):
        verdict, reason = vp.decide(self.analysis("1.1.0", "1.0.0"))
        self.assertEqual(verdict, "fail")
        self.assertIn("version did not increase", reason)

    def test_existing_plugin_accepts_a_version_increase(self):
        self.assertEqual(vp.decide(self.analysis("0.1.0", "0.2.0")), ("accept", None))


if __name__ == "__main__":
    unittest.main()
