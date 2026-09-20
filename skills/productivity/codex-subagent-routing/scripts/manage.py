#!/usr/bin/env python3
"""Install four Codex role files and a managed delegation section."""
import sys
if sys.version_info < (3, 11):
    sys.exit('Python 3.11+ required; use an existing python3.12 interpreter.')
import argparse
import difflib
import os
from pathlib import Path
import re
import shutil
import tempfile
import tomllib
from uuid import uuid4

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
START = '<!-- codex-subagent-routing:start -->'
END = '<!-- codex-subagent-routing:end -->'
NAMES = ('luna-subagent', 'terra-subagent', 'sol-subagent', 'astra-subagent')


def validate(raw, name):
    data = tomllib.loads(raw.decode('utf-8'))
    for key in ('name', 'description', 'developer_instructions', 'model', 'model_reasoning_effort'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'{name}: missing or invalid {key}')
    if data['name'] != name:
        raise ValueError(f'{name}: name field does not match filename')
    return data


def policy_content(old, section, replace):
    text = old.decode('utf-8')
    block = START + '\n' + section.rstrip() + '\n' + END
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1 or text.index(START) >= text.index(END):
            raise ValueError('Malformed or duplicate managed markers in AGENTS.md')
        a, b = text.index(START), text.index(END) + len(END)
        outside = text[:a] + text[b:]
        if re.search(r'^## 子 Agent 委派\s*$', outside, re.M):
            raise ValueError('Duplicate delegation section outside managed block')
        return (text[:a] + block + text[b:]).encode()
    headings = list(re.finditer(r'^## 子 Agent 委派[^\S\n]*$', text, re.M))
    if len(headings) > 1:
        raise ValueError('Duplicate legacy delegation sections')
    if headings:
        a = headings[0].start()
        following = re.search(r'^#{1,2} ', text[headings[0].end():], re.M)
        b = headings[0].end() + following.start() if following else len(text)
        legacy = text[a:b]
        if legacy.strip() != section.strip() and not replace:
            raise ValueError('Legacy delegation section differs; review show --replace-existing before replacing')
        # Keep separators before the next heading exactly as found.
        trailing = legacy[len(legacy.rstrip()):]
        return (text[:a] + block + trailing + text[b:]).encode()
    separator = '' if not text or text.endswith('\n\n') else '\n' if text.endswith('\n') else '\n\n'
    return (text + separator + block + '\n').encode()


def plan(home, replace=False):
    changes, records = [], []
    for name in NAMES:
        wanted = (ASSETS / 'agents' / (name + '.toml')).read_bytes()
        validate(wanted, name)
        target = home / 'agents' / (name + '.toml')
        old = target.read_bytes() if target.exists() else None
        actual = validate(old, name) if old is not None else None
        if old is not None and old != wanted and not replace:
            records.append(f'KEEP customized {name}: {actual["model"]} / {actual["model_reasoning_effort"]}')
        else:
            if old != wanted:
                changes.append((target, old, wanted))
            data = actual or validate(wanted, name)
            records.append(f'{"MISSING" if old is None else "CONFIGURED"} {name}: {data["model"]} / {data["model_reasoning_effort"]}')
    target = home / 'AGENTS.md'
    old = target.read_bytes() if target.exists() else None
    section = (ASSETS / 'delegation.md').read_text()
    wanted = policy_content(old or b'', section, replace)
    if old != wanted:
        changes.append((target, old, wanted))
    return changes, records, section


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['show', 'check', 'apply'])
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', '~/.codex')))
    parser.add_argument('--replace-existing', action='store_true')
    args = parser.parse_args()
    home = args.codex_home.expanduser().resolve()
    print('Codex home:', home)
    try:
        changes, records, section = plan(home, args.replace_existing)
        for record in records:
            print(record)
        if (home / 'AGENTS.override.md').exists():
            print('WARNING: AGENTS.override.md exists; inspect whether it shadows global AGENTS.md.')
        if args.action == 'check':
            pending = []
            for path, old, new in changes:
                # Exact legacy content is valid before managed-marker adoption.
                if path.name == 'AGENTS.md' and old is not None and START.encode() not in old and section.strip() in old.decode():
                    continue
                pending.append(path)
            if pending:
                print('CHECK FAILED: changes needed:', ', '.join(str(p) for p in pending))
                return 1
            print('CHECK PASS: files valid; customized roles may differ from bundled defaults. Runtime not tested.')
            return 0
        for path, old, new in changes:
            print(''.join(difflib.unified_diff((old or b'').decode().splitlines(True), new.decode().splitlines(True), fromfile=str(path), tofile=str(path) + ' (proposed)')), end='')
        if args.action == 'show':
            print(f'Planned changes: {len(changes)}')
            return 0
        # All parsing/conflict checks have completed before any mutation.
        for path, old, new in changes:
            current = path.read_bytes() if path.exists() else None
            if current != old:
                raise ValueError(f'Concurrent modification: {path}; rerun show')
        for path, old, new in changes:
            path.parent.mkdir(parents=True, exist_ok=True)
            if old is not None:
                backup = path.with_name(path.name + '.bak.' + uuid4().hex)
                shutil.copy2(path, backup)
                print('BACKUP', backup)
            fd, temp = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(new)
                if old is not None:
                    os.chmod(temp, path.stat().st_mode & 0o777)
                os.replace(temp, path)
            finally:
                if os.path.exists(temp):
                    os.unlink(temp)
            print('WROTE', path)
        print(f'APPLY PASS: {len(changes)} file(s) changed')
        return 0
    except (OSError, ValueError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
