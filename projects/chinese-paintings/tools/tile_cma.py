import json, os, math, subprocess, pyvips, time
CAP = 30e6
OUT = '/home/claude/homepage/chinese-paintings/tiles'; TMP = '/home/claude/cp/dl'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
d = {r['id']: r for r in json.load(open('paintings_raw.json'))}
ids = json.load(open('cma_tile_list.json'))
order = ['Six Dynasties','Sui','Tang','Five Dynasties','Northern Song','Song (general)','Jin','Liao','Southern Song','Yuan','Ming','Qing','Unknown']
ids.sort(key=lambda i: (order.index(d[i]['dynasty']) if d[i]['dynasty'] in order else 99, -(d[i]['images'][0]['fw']*d[i]['images'][0]['fh'])))
done = json.load(open('tiled.json')) if os.path.exists('tiled.json') else {}
for rid in ids:
    key = f'{rid}_0'
    if key in done: continue
    url = d[rid]['images'][0]['full']; f = os.path.join(TMP, key + '.tif')
    for t in range(3):
        rc = subprocess.run(['curl', '-s', '-m', '1200', '-o', f, '-w', '%{http_code}', url], capture_output=True, text=True).stdout
        if rc == '200': break
        time.sleep(10)
    else:
        print('fail', key, flush=True); continue
    try:
        img = pyvips.Image.new_from_file(f)
        if img.width * img.height > CAP:
            img = img.resize(math.sqrt(CAP / (img.width * img.height)))
        if img.hasalpha(): img = img.flatten(background=[255, 255, 255])
        if img.interpretation not in ('srgb',) : img = img.colourspace('srgb')
        if img.format != 'uchar': img = img.cast('uchar')
        img.dzsave(os.path.join(OUT, key), tile_size=1024, overlap=1, suffix='.jpg[Q=72,optimize_coding,strip]', depth='onetile')
        done[key] = [img.width, img.height]; json.dump(done, open('tiled.json', 'w'))
        print('ok', key, img.width, img.height, flush=True)
    except Exception as e:
        print('vips fail', key, str(e)[:200], flush=True)
    finally:
        if os.path.exists(f): os.remove(f)
print('ALL DONE', flush=True)
