#!/usr/bin/env python3
"""Regenerate the offline file list in sw.js.

Run from anywhere after adding, removing or changing any file in this folder:

    python3 build.py
"""
import hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
SKIP = {'sw.js', 'build.py', 'README.md'}
# Needed before the page can open offline; everything else fills in afterwards.
CORE_DIRS = ('fonts/', 'vendor/', 'icons/')
CORE_FILES = {'index.html', 'manifest.webmanifest', 'palettes.json', 'canvas.json'}

files = {}
for f in sorted(ROOT.rglob('*')):
    rel = f.relative_to(ROOT).as_posix()
    if f.is_file() and rel not in SKIP and not rel.startswith('.'):
        files[rel] = hashlib.sha256(f.read_bytes()).hexdigest()[:10]
core = [p for p in files if p in CORE_FILES or p.startswith(CORE_DIRS)]

block = ('// BEGIN FILES\n'
         f'const FILES = {json.dumps(files, indent=0)};\n'
         f'const CORE = {json.dumps(core)};\n'
         '// END FILES')
sw = ROOT / 'sw.js'
sw.write_text(re.sub(r'// BEGIN FILES.*?// END FILES', lambda _: block, sw.read_text(), flags=re.S))
print(f'{len(files)} files, {len(core)} core')
