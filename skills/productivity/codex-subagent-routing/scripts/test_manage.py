#!/usr/bin/env python3
"""Exercise installation only in disposable Codex homes."""
import sys
if sys.version_info < (3, 11):
    sys.exit('Python 3.11+ required.')
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('manage.py')
ASSETS = SCRIPT.parent.parent / 'assets'

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def run_cli(self, action, *extra, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), action, '--codex-home', str(self.home), *extra], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def snapshot(self):
        return {str(p.relative_to(self.home)): p.read_bytes() for p in self.home.rglob('*') if p.is_file()}

    def test_fresh_show_install_idempotence(self):
        self.run_cli('show')
        self.assertEqual(self.snapshot(), {})
        self.run_cli('check', ok=False)
        self.run_cli('apply')
        self.run_cli('check')
        before = self.snapshot()
        self.run_cli('apply')
        self.assertEqual(before, self.snapshot())

    def test_custom_role_preserved_then_replaced_with_backup(self):
        target = self.home / 'agents/luna-subagent.toml'
        target.parent.mkdir()
        custom = (ASSETS / 'agents/luna-subagent.toml').read_bytes().replace(b'"max"', b'"medium"')
        target.write_bytes(custom)
        self.run_cli('apply')
        self.assertEqual(target.read_bytes(), custom)
        self.assertIn('KEEP customized', self.run_cli('check'))
        self.run_cli('apply', '--replace-existing')
        self.assertEqual(target.read_bytes(), (ASSETS / 'agents/luna-subagent.toml').read_bytes())
        self.assertTrue(any(p.read_bytes() == custom for p in target.parent.glob('*.bak.*')))

    def test_legacy_adoption_preserves_other_sections(self):
        section = (ASSETS / 'delegation.md').read_bytes()
        prefix, suffix = b'# Custom\nKeep exact spaces.  \n\n', b'\n## Other\nKeep this too.\n'
        target = self.home / 'AGENTS.md'
        original = prefix + section + suffix
        target.write_bytes(original)
        self.run_cli('apply')
        result = target.read_bytes()
        self.assertTrue(result.startswith(prefix))
        self.assertTrue(result.endswith(suffix))
        self.assertEqual(result.count(b'## \xe5\xad\x90 Agent'), 1)
        self.assertTrue(any(p.read_bytes() == original for p in self.home.glob('*.bak.*')))
        self.run_cli('check')

    def test_conflicting_legacy_requires_replacement(self):
        (self.home / 'AGENTS.md').write_text('## 子 Agent 委派\nCustom policy\n\n## Other\nkeep\n')
        before = self.snapshot()
        self.run_cli('apply', ok=False)
        self.assertEqual(before, self.snapshot())
        self.run_cli('apply', '--replace-existing')
        self.assertTrue((self.home / 'AGENTS.md').read_text().endswith('## Other\nkeep\n'))

    def test_malformed_inputs_do_not_partially_write(self):
        for text in ['<!-- codex-subagent-routing:start -->', '<!-- codex-subagent-routing:end -->\n<!-- codex-subagent-routing:start -->']:
            (self.home / 'AGENTS.md').write_text(text)
            before = self.snapshot()
            self.run_cli('apply', ok=False)
            self.assertEqual(before, self.snapshot())
        (self.home / 'AGENTS.md').unlink()
        target = self.home / 'agents/astra-subagent.toml'
        target.parent.mkdir()
        target.write_text('not = [valid')
        before = self.snapshot()
        self.run_cli('apply', ok=False)
        self.assertEqual(before, self.snapshot())

    def test_override_warning(self):
        (self.home / 'AGENTS.override.md').write_text('Custom override')
        self.assertIn('WARNING', self.run_cli('apply'))
        self.assertEqual((self.home / 'AGENTS.override.md').read_text(), 'Custom override')

if __name__ == '__main__':
    unittest.main()
