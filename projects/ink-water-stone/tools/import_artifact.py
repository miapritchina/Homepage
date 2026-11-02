#!/usr/bin/env python3
"""Turn the Claude artifact's index.html into this folder's standalone index.html.

Usage:  python3 tools/import_artifact.py <downloaded artifact index.html>

It moves the head into a real <head>, swaps Google Fonts and the cdnjs JSZip for
local copies, replaces the artifact-only download API with plain browser saving
(share sheet on touch devices), and adds the install/offline wiring. Each step
asserts it matched exactly once, so a changed artifact fails loudly instead of
producing a half-converted page. Afterwards run tools/subset_fonts.py (if new
Chinese characters appeared) and build.py.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
s = open(sys.argv[1], encoding='utf8').read()


def cut(start, end_marker, include_end=True):
    """Remove and return the text from `start` up to `end_marker`."""
    global s
    i = s.index(start)
    j = s.index(end_marker, i) + (len(end_marker) if include_end else 0)
    piece = s[i:j]
    s = s[:i] + s[j:]
    return piece


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)


# 1. A proper document head
s = s[s.index('\n') + 1:]  # artifact runtime's wrapper line; its <style> is kept below
wrapper_style = open(sys.argv[1], encoding='utf8').read().split('\n', 1)[0]
wrapper_style = wrapper_style[wrapper_style.index('<style>'):wrapper_style.index('</style>') + 8]
rep('<title>Ink, Water, Stone</title>\n', '')
rep('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
rep('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n', '')
cut('<link rel="stylesheet" href="https://fonts.googleapis.com', '\n')
main_style = cut('<style>', '</style>')
theme = cut('<script>try{var _st', '</script>')

# iPad first: one brush per row in the dictionary at every width
assert main_style.count('@media (min-width:560px){.dgrid{grid-template-columns:1fr 1fr}}\n') == 1
main_style = main_style.replace('@media (min-width:560px){.dgrid{grid-template-columns:1fr 1fr}}\n', '')

head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Ink, Water, Stone</title>
<meta name="description" content="A field guide for painting Chinese ink in Procreate: paper, ink, pigments, brushes and step-by-step projects.">
<meta name="theme-color" content="#E6E3D9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1C1D21" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Ink Water Stone">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="icon" href="icons/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="stylesheet" href="fonts/fonts.css">
{wrapper_style}
{main_style}
<style>
#toast{{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:25;background:var(--ink);color:var(--paper);border-radius:999px;padding:10px 16px;font-size:13.5px;box-shadow:0 6px 20px rgba(0,0,0,.25);max-width:calc(100% - 32px);text-align:center}}
#toast[hidden]{{display:none!important}}
.offline{{display:block;margin-top:6px}}
</style>
{theme}
</head>
<body>
'''
s = head + s.lstrip()

# 2. Local JSZip
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>',
    '<script src="vendor/jszip.min.js"></script>')

# 3. Downloads: plain browser saving instead of the artifact runtime
cut("(function(){\n  const note=document.getElementById('dlnote');", '// tabs, cross-tab links', include_end=False)
rep('// tabs, cross-tab links', '''// save a generated or bundled file: share sheet on phones and tablets (Save to Files, Procreate), a normal download elsewhere
const toast=document.getElementById('toast');let toastT=null;
function say(t){toast.textContent=t;toast.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>{toast.hidden=true},5000)}
async function saveFile(name,blob){
  const file=new File([blob],name,{type:blob.type||'application/octet-stream'});
  const touch=matchMedia('(pointer:coarse)').matches;
  if(touch&&navigator.canShare&&navigator.canShare({files:[file]})){
    try{await navigator.share({files:[file]});return}catch(e){if(e&&e.name==='AbortError')throw {code:'declined'}}
  }
  const url=URL.createObjectURL(file),a=document.createElement('a');
  a.href=url;a.download=name;document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),60000);
}
document.querySelectorAll('button.dl').forEach(b=>b.addEventListener('click',async()=>{
  const label=b.textContent; b.disabled=true; b.textContent=b.dataset.gen?'Building canvas…':'Preparing…';
  try{
    let data;
    if(b.dataset.gen){ if(typeof JSZip==='undefined') throw {code:'lib'}; data=await makeCanvas(b.dataset.gen); }
    else if(b.dataset.pal){ if(typeof JSZip==='undefined') throw {code:'lib'}; data=await makePalettes(); }
    else { const r=await fetch(b.dataset.path); if(!r.ok) throw {code:'fetch'}; data=await r.blob(); }
    await saveFile(b.dataset.name,data);
    b.textContent='Saved'; setTimeout(()=>{b.textContent=label},2500); return;
  }catch(e){
    const c=e&&e.code;
    if(c==='declined'){} else if(c==='fetch'||c==='lib'){say('A file did not load. Connect once so the guide can finish saving itself, then try again.')}
    else {say('This file could not be saved. Try again.')}
  } finally { b.disabled=false; if(/…$/.test(b.textContent)) b.textContent=label }
}));

// tabs, cross-tab links''')
assert 'window.claude' not in s, 'artifact still calls window.claude somewhere new'

# 4. Toast, offline status, service worker
rep('<div id="pop" hidden role="dialog" aria-live="polite"></div>',
    '<div id="pop" hidden role="dialog" aria-live="polite"></div>\n<div id="toast" hidden role="status"></div>')
rep('photos and paintings are credited in Notes.</p>',
    'photos and paintings are credited in Notes.<span class="offline" id="offline" hidden></span></p>')
rep('\n</body></html>', '''<script>
// offline app: the service worker stores the whole guide on first visit
if('serviceWorker' in navigator){
  const off=document.getElementById('offline');
  navigator.serviceWorker.addEventListener('message',e=>{const d=e.data||{};
    if(d.type==='progress'){off.hidden=false;off.textContent=d.done>=d.total?'Saved for offline use.':'Saving for offline use: '+d.done+' of '+d.total+' files…'}});
  addEventListener('load',()=>navigator.serviceWorker.register('sw.js').then(()=>navigator.serviceWorker.ready).then(r=>r.active&&r.active.postMessage('status')).catch(()=>{}));
}
</script>
</body>
</html>
''')
for bad in ('fonts.googleapis', 'fonts.gstatic', 'cdnjs.cloudflare'):
    assert bad not in s, bad

(ROOT / 'index.html').write_text(s, encoding='utf8')
print('wrote', ROOT / 'index.html')
