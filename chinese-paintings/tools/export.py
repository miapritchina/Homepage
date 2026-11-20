import json, math, re, os, urllib.parse
from artists import A
d = json.load(open('paintings_raw.json'))
lo = json.load(open('linkonly_raw.json'))
tiled = json.load(open('tiled.json')) if os.path.exists('tiled.json') else {}
OUT = '/home/claude/homepage/chinese-paintings/data'
os.makedirs(OUT, exist_ok=True)
STEPS = [500, 960, 1280, 1920, 3840]

def strip_q(u): return u.split('?')[0] if u else u
def cthumb(url, w):
    url = strip_q(url); p = url.split('/wikipedia/commons/')[1]; name = p.split('/')[-1]
    if name.lower().endswith(('.tif', '.tiff')): return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{p}/lossy-page1-{w}px-{name}.jpg'
    if name.lower().endswith('.gif'): return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{p}/{w}px-{name}.png'
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{p}/{w}px-{name}'

out = []
for r in d:
    ims = []; mp = r.get('mp')
    for n, im in enumerate(r['images']):
        key = f"{r['id']}_{n}"
        if key in tiled:
            w, h = tiled[key]; ims.append({'t': 'dzi', 'u': f'tiles/{key}.dzi'})
            if n == 0: mp = round(w * h / 1e6, 1)
        elif im['t'] == 'big' or (r['src'] == 'Commons' and im.get('w') and im['w'] * im['h'] > 45e6):
            # too large (or TIFF) for a browser: ask Wikimedia for a scaled JPEG of ~45 MP
            w, h = im['w'], im['h']
            tw = int(min(w - 1, w * math.sqrt(min(1, 45e6 / (w * h)))))
            ims.append({'t': 'img', 'u': cthumb(im['u'], tw)})
            if n == 0: mp = round(tw * (h * tw / w) / 1e6, 1)
        else:
            x = {'t': im['t'], 'u': strip_q(im['u'])}
            ims.append(x)
    th = r['thumb']
    if r['src'] == 'Commons': th = cthumb(r['images'][0]['u'], 500)
    ar = None
    if r.get('px') and r['px'][0]: ar = round(r['px'][0] / r['px'][1], 3)
    elif r['images'][0].get('w'): ar = round(r['images'][0]['w'] / r['images'][0]['h'], 3)
    tt = r['title']
    if r.get('titleZh') and re.search(r'[A-Za-z]', tt): tt = re.sub(r'\s*[\u3400-\u9fff][\u3400-\u9fff\s·、（）()]*$', '', tt).strip() or tt
    rec = dict(i=r['id'], t=tt, z=r.get('titleZh') or '', a=r['artist'], az=r.get('artistZh') or '', ad=r.get('artistDates') or '',
               s=r.get('school'), at=r['attribution'], ap=r.get('approach'), d=r['dynasty'], y1=r['y1'], y2=r['y2'], c=r.get('century'),
               dt=r.get('date') or '', f=r['format'], su=r['support'], p=r['palette'], g=r['genre'], tg=r['tags'], se=r['season'],
               m=r['museum'], md=r.get('medium') or '', dm=r.get('dims') or '', cr=r.get('credit') or '', l=r.get('link'), cm=r.get('commons'),
               de=(r.get('desc') or '')[:1600], dy=r.get('didyouknow') or '', ins=r.get('inscription') or '', th=th, im=ims, mp=mp, ar=ar, lic=r.get('license'))
    out.append({k: v for k, v in rec.items() if v not in (None, '', [], False)})

for x in lo:
    href = x.get('zhwiki') or x.get('enwiki') or f"https://www.wikidata.org/wiki/{x['q']}"
    y = x.get('y')
    rec = dict(i='lo' + x['q'], lo=1, t=x['title'], z=x.get('zh') or '', a=x.get('creator') or 'Unidentified artist', az=x.get('creatorZh') or '', m=x['museum'], l=href,
               y1=y, y2=y, g=x['genre'], tg=x['tags'], se=x['season'], d=x['dyn'], c=x.get('century'), s=x.get('school'), at='See museum')
    out.append({k: v for k, v in rec.items() if v not in (None, '', [])})
print(len(out))
json.dump(out, open(f'{OUT}/paintings.json', 'w'), ensure_ascii=False, separators=(',', ':'))
arts = {}
for k, v in A.items():
    if v['note']: arts[v['name']] = {'zh': v['zh'], 'dates': v['dates'], 'note': v['note'], 'school': v['school']}
json.dump(arts, open(f'{OUT}/artists.json', 'w'), ensure_ascii=False)
if not os.path.exists(f'{OUT}/notes.json'): json.dump({}, open(f'{OUT}/notes.json', 'w'))
print(os.path.getsize(f'{OUT}/paintings.json') / 1e6, 'MB')
from notes_src import N
json.dump(N, open(f'{OUT}/notes.json', 'w'), ensure_ascii=False)
print('notes', len(N))
