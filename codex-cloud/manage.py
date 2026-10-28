#!/usr/bin/env python3
"""Verify the vendored bundle; copy into another Git repository with explicit --apply."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent

def verify():
    manifest = json.loads((ROOT / 'codex-cloud/manifest.json').read_text(encoding='utf-8'))
    expected = manifest['files']
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / '.agents/skills').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    if actual != set(expected):
        raise ValueError('Missing or unexpected skill files: '+str(actual ^ set(expected)))
    legal = manifest['legal_files']
    for rel, digest in {**expected, **legal}.items():
        p = ROOT / rel
        if p.is_symlink() or not p.resolve().is_relative_to(ROOT):
            raise ValueError('Unsafe source path: '+rel)
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            raise ValueError('Hash mismatch: '+rel)
    for skill in manifest['selected']:
        p = ROOT / '.agents/skills' / ('anthropic-'+skill) / 'SKILL.md'
        s = p.read_text(encoding='utf-8')
        if not s.startswith('---\n') or '\n---' not in s[4:]:
            raise ValueError('Missing frontmatter: '+str(p))
        header = s.split('---', 2)[1]
        if not re.search(r'^name: anthropic-'+re.escape(skill)+r'$', header, re.M):
            raise ValueError('Invalid name: '+skill)
        if not re.search(r'^description: .+', header, re.M):
            raise ValueError('Missing description: '+skill)
    print('PASS: 5 skill manifests and '+str(len(expected))+' SHA-256 hashes')
    return {**expected, **legal}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-repo', type=Path)
    parser.add_argument('--apply', action='store_true', help='Copy after all collision checks; default is dry-run')
    args = parser.parse_args()
    files = verify()
    if args.apply and args.target_repo is None:
        parser.error('--apply requires --target-repo')
    if args.target_repo is None:
        return
    target = args.target_repo.resolve(strict=True)
    if not (target / '.git').exists():
        raise ValueError('Target must be the root of a Git repository')
    # Preflight every path before any write. Preserve any different existing file.
    pending = []
    for rel, digest in files.items():
        dest = target / rel
        if not dest.resolve().is_relative_to(target):
            raise ValueError('Target path escapes repository: '+rel)
        if dest.exists():
            if not dest.is_file() or hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
                raise ValueError('Refusing to overwrite existing content: '+rel)
        else:
            pending.append((ROOT / rel, dest))
    # New bundle files must not leave old files inside a skill directory.
    for name in json.loads((ROOT / 'codex-cloud/manifest.json').read_text())['selected']:
        folder = target / '.agents/skills' / ('anthropic-'+name)
        if folder.exists():
            extra = [p for p in folder.rglob('*') if p.is_file() and p.relative_to(target).as_posix() not in files]
            if extra:
                raise ValueError('Unexpected existing skill files: '+str(extra))
    if args.apply:
        for source, dest in pending:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    print(('APPLIED' if args.apply else 'DRY RUN')+': '+str(len(pending))+' files; target='+str(target))
    print('Commit the resulting .agents/skills files to a branch used by Cloud tasks for durable reuse.')

if __name__ == '__main__':
    main()
