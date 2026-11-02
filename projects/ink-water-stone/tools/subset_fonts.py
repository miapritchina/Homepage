#!/usr/bin/env python3
"""Rebuild fonts/ with only the characters index.html and palettes.json use.

Usage:  python3 tools/subset_fonts.py      (needs: pip install fonttools brotli)

Downloads Fraunces, Literata and Noto Serif SC from Google Fonts, subsets each
to the text of the guide (Latin fonts to Latin, Noto Serif SC to Chinese), and
writes woff2 files plus fonts/fonts.css. Run it whenever the guide gains new
Chinese characters, or they fall back to a system font.
"""
import pathlib, re, subprocess, tempfile, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300'
       '&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;0,7..72,600;1,7..72,400;1,7..72,600'
       '&family=Noto+Serif+SC:wght@500;600;700&display=swap')

text = (ROOT / 'index.html').read_text('utf8') + (ROOT / 'palettes.json').read_text('utf8')
text += re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), text)  # \uXXXX in scripts
chars = {c for c in text if ord(c) >= 0x20} | {chr(c) for c in range(0x20, 0x7f)} | set('…–—‘’“”·×→←↑↓•°©')
cjk = ''.join(sorted(c for c in chars if ord(c) >= 0x2e80))
latin = ''.join(sorted(c for c in chars if ord(c) < 0x2e80))

with tempfile.TemporaryDirectory() as tmp:
    tmp = pathlib.Path(tmp)
    (tmp / 'cjk.txt').write_text(cjk, 'utf8')
    (tmp / 'latin.txt').write_text(latin, 'utf8')
    # A plain user agent gets full TTF files rather than pre-split woff2 slices.
    css = urllib.request.urlopen(urllib.request.Request(CSS, headers={'User-Agent': 'curl'})).read().decode()
    faces = []
    for block in re.findall(r'@font-face\s*{[^}]*}', css):
        family = re.search(r"font-family: '([^']+)'", block).group(1)
        style = re.search(r'font-style: (\w+)', block).group(1)
        weight = re.search(r'font-weight: (\d+)', block).group(1)
        name = f"{family.replace(' ', '')}-{weight}{'i' if style == 'italic' else ''}"
        src = tmp / (name + '.ttf')
        urllib.request.urlretrieve(re.search(r'url\(([^)]+)\)', block).group(1), src)
        subset = 'cjk.txt' if family == 'Noto Serif SC' else 'latin.txt'
        subprocess.run(['pyftsubset', str(src), f'--text-file={tmp / subset}', '--flavor=woff2',
                        '--layout-features=*', f'--output-file={ROOT / "fonts" / (name + ".woff2")}'], check=True)
        faces.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
                     f"font-display:swap;src:url({name}.woff2) format('woff2')}}")
(ROOT / 'fonts' / 'fonts.css').write_text('\n'.join(faces) + '\n')
print(f'{len(faces)} faces, {len(cjk)} Chinese characters')
