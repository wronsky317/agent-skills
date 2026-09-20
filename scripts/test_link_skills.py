#!/usr/bin/env python3
"""Exercise linking and Codex setup only against temporary directories."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'skills/productivity/codex-subagent-routing'


class LinkSkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='link skills ')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.skills = self.base / 'library'
        shutil.copytree(SOURCE, self.skills / 'codex-subagent-routing')
        self.home = self.base / 'codex home'
        self.home.mkdir()
        self.config = self.base / 'agents.conf'
        self.config.write_text(f'codex|{self.home}/skills\n')
        self.env = dict(os.environ, AGENT_SKILLS_ROOT=str(self.skills),
                        AGENT_SKILLS_CONFIG=str(self.config),
                        AGENT_SKILLS_SYSTEM_DIR=str(self.base / 'no-system'),
                        AGENT_SKILLS_PYTHON=sys.executable)

    def run_link(self, success=True):
        result = subprocess.run(['bash', str(ROOT / 'scripts/link-skills.sh')],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_install_and_repeat_preserves_customizations(self):
        policy = self.home / 'AGENTS.md'
        policy.write_text('# Personal instructions\nKeep this.\n')
        self.run_link()
        self.assertEqual(len(list((self.home / 'agents').glob('*.toml'))), 4)
        self.assertTrue((self.home / 'skills/codex-subagent-routing').is_symlink())
        self.assertTrue(policy.read_text().startswith('# Personal instructions\nKeep this.\n'))
        self.assertEqual(len(list(self.home.glob('AGENTS.md.bak.*'))), 1)
        role = self.home / 'agents/luna-subagent.toml'
        role.write_text(role.read_text().replace('model_reasoning_effort = "max"',
                                                'model_reasoning_effort = "high"'))
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in [policy, *self.home.glob('agents/*.toml')]}
        output = self.run_link()
        self.assertIn('APPLY PASS: 0 file(s) changed', output)
        self.assertEqual(before, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before})

    def test_no_codex_target(self):
        self.config.write_text(f'qoder|{self.base}/qoder/skills\n')
        self.run_link()
        self.assertFalse((self.home / 'agents').exists())

    def test_absent_codex_home(self):
        self.home.rmdir()
        self.assertIn('Codex home does not exist', self.run_link())
        self.assertFalse((self.home / 'agents').exists())

    def test_missing_skill(self):
        shutil.rmtree(self.skills / 'codex-subagent-routing')
        self.assertIn('skill not found', self.run_link())
        self.assertFalse((self.home / 'AGENTS.md').exists())

    def test_existing_directory_with_missing_role(self):
        self.run_link()
        role = self.home / 'agents/terra-subagent.toml'
        role.unlink()
        self.run_link()
        self.assertTrue(role.exists())

    def test_conflicting_policy_fails_before_role_install(self):
        policy = self.home / 'AGENTS.md'
        policy.write_text('## 子 Agent 委派\nMy custom policy.\n')
        before = policy.read_bytes()
        self.assertIn('Legacy delegation section differs', self.run_link(False))
        self.assertEqual(policy.read_bytes(), before)
        self.assertFalse((self.home / 'agents').exists())

    def test_identical_legacy_policy_not_duplicated(self):
        policy = self.home / 'AGENTS.md'
        policy.write_bytes((SOURCE / 'assets/delegation.md').read_bytes())
        self.run_link()
        self.assertEqual(policy.read_text().count('## 子 Agent 委派'), 1)

    def test_malformed_role_fails_without_other_writes(self):
        (self.home / 'agents').mkdir()
        role = self.home / 'agents/luna-subagent.toml'
        role.write_text('invalid = [')
        self.run_link(False)
        self.assertEqual(list((self.home / 'agents').iterdir()), [role])
        self.assertFalse((self.home / 'AGENTS.md').exists())


if __name__ == '__main__':
    unittest.main()
