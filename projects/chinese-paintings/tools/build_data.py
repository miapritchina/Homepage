import json, re, html, collections, urllib.parse, hashlib
from artists import A, ZH

def clean(s):
    if not s: return ''
    s = re.sub(r'<[^>]+>', ' ', str(s)); s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

HAN = re.compile(r'[㐀-鿿豈-﫿]+[㐀-鿿豈-﫿\s·、（）()]*')
def zh_of(s):
    m = HAN.findall(s or '');  return ''.join(m).strip() if m else ''

# ---------- artist matching ----------
KEYS = sorted(A.keys(), key=len, reverse=True)
def match_artist(text):
    t = (text or '').lower().replace('ü', 'u').replace('–', '-')
    t2 = (text or '').lower()
    for z in sorted(ZH, key=len, reverse=True):
        if z in (text or ''): return ZH[z]
    for k in KEYS:
        kk = k.replace('ü', 'u')
        if re.search(r'(^|[^a-z])' + re.escape(kk) + r'($|[^a-z])', t) or re.search(r'(^|[^a-z])' + re.escape(k) + r'($|[^a-z])', t2):
            return k
    return None

def attribution(text):
    t = (text or '').lower()
    if not t or t.strip() in ('', 'china', 'tibet or china', 'unidentified', 'artist unknown', 'unidentified artist', 'unknown'): return 'Unidentified artist'
    if 'formerly attributed' in t: return 'Formerly attributed'
    if 'attributed' in t or '(傳)' in t or '傳' in t[:4]: return 'Attributed'
    if 'after ' in t or 'copy' in t or 'style of' in t or 'follower' in t or 'workshop' in t or 'school of' in t or ('unidentified' in t and '|' in t): return 'After / in the style of'
    if 'unidentified' in t or 'unknown' in t: return 'Unidentified artist'
    return 'Signed or firmly attributed'

# ---------- dates & dynasties ----------
DYN = [(-1e9, 220, 'Han & earlier'), (220, 581, 'Six Dynasties'), (581, 618, 'Sui'), (618, 907, 'Tang'),
       (907, 960, 'Five Dynasties'), (960, 1127, 'Northern Song'), (1127, 1279, 'Southern Song'),
       (1279, 1368, 'Yuan'), (1368, 1644, 'Ming'), (1644, 1913, 'Qing')]
DYN_ORDER = [d[2] for d in DYN] + ['Jin', 'Liao', 'Xixia']
def dyn_from_text(t):
    t = (t or '').lower()
    for k, v in [('northern song', 'Northern Song'), ('southern song', 'Southern Song'), ('five dynasties', 'Five Dynasties'),
                 ('jin dynasty', 'Jin'), ('liao', 'Liao'), ('yuan', 'Yuan'), ('ming', 'Ming'), ('qing', 'Qing'),
                 ('tang', 'Tang'), ('sui', 'Sui'), ('six dynasties', 'Six Dynasties'), ('song', 'Song')]:
        if re.search(r'\b' + k + r'\b', t): return v
    return None
def dyn_from_year(y):
    for a, b, n in DYN:
        if a <= y < b: return n
def parse_years(t):
    ys = [int(y) for y in re.findall(r'(?<!\d)(\d{3,4})(?!\d)', t or '') if 300 < int(y) < 1950]
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)\s*(?:–|-|to)?\s*(?:(\d{1,2})(?:st|nd|rd|th))?\s*century', (t or '').lower())
    if not ys and m:
        c1 = int(m.group(1)); c2 = int(m.group(2) or c1)
        return (c1 - 1) * 100, c2 * 100
    if ys: return min(ys), max(ys)
    return None, None
def century(y):
    if y is None: return None
    c = y // 100 + 1
    suf = 'th' if 10 <= c % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(c % 10, 'th')
    return f'{c}{suf} century'

# ---------- format / material ----------
def fmt(t):
    t = (t or '').lower()
    for k, v in [('handscroll', 'Handscroll'), ('hanging scroll', 'Hanging scroll'), ('fan', 'Fan'), ('album', 'Album leaf'),
                 ('screen', 'Screen'), ('wall painting', 'Wall painting'), ('mural', 'Wall painting'), ('banner', 'Banner'),
                 ('panel', 'Panel'), ('scroll', 'Hanging scroll'), ('leaf', 'Album leaf')]:
        if k in t: return v
    return 'Other'
def support(t):
    t = (t or '').lower()
    if 'gold paper' in t or 'gold-flecked' in t or 'gold-speckled' in t or 'flecked' in t: return 'Gold-flecked paper'
    if 'satin' in t: return 'Satin'
    if 'pith' in t: return 'Pith paper'
    if 'silk' in t: return 'Silk'
    if 'paper' in t: return 'Paper'
    if 'plaster' in t or 'clay' in t or 'wall' in t: return 'Wall / plaster'
    if 'hemp' in t or 'ramie' in t or 'cotton' in t or 'linen' in t: return 'Hemp / cloth'
    return 'Other'
def palette(t, title):
    t = (t or '').lower(); ti = (title or '').lower()
    out = []
    if 'blue-and-green' in ti or 'blue-green' in ti or 'blue and green' in ti or 'blue-and-green' in t: out.append('Blue-green')
    if 'gold' in t: out.append('Gold')
    if 'color' in t or 'colour' in t or 'pigment' in t:
        out.append('Light colour' if ('light color' in t or 'slight color' in t or 'pale color' in t) else 'Ink & colour')
    elif 'ink' in t: out.append('Ink only')
    if not out: out.append('Unknown')
    return out

# ---------- subjects ----------
SUBJ = {
 'Landscape': r'landscape|mountain|river|stream|lake|waterfall|cascade|peak|cliff|valley|hills|gorge|cloud|mist|scenery|views? of|riverbank|shore|islet|retreat|hermitage|thatched|village|travell?ers?',
 'Bird-and-flower': r'bird|flower|blossom|peon|lotus|plum|bamboo|orchid|chrysanthem|narcissus|magnolia|camellia|crane|sparrow|magpie|egret|heron|duck|mandarin|goose|geese|swallow|kingfisher|parrot|rooster|hen|quail|insect|butterfl|cicada|dragonfl|fruit|vegetable|grape|melon|lily|hibiscus|wisteria|rose|pheasant|eagle|hawk|falcon|owl|pine|cypress|willow|tree|rock|garden flowers|grass',
 'Figure': r'figure|scholar|lady|ladies|women|woman|beaut|portrait|immortal|luohan|lohan|arhat|guanyin|bodhisattva|buddha|emperor|official|child|boy|fisherm|herd|sage|poet|gathering|monk|daoist|taoist|god|goddess|king|queen|consort|maiden|man |men |people|musician|zhong kui|demon|ghost|servant|figures',
 'Animals': r'horse|ox|oxen|buffalo|tiger|cat\b|cats\b|dog|monkey|gibbon|deer|squirrel|dragon|goat|sheep|rabbit|hare|lion|elephant|camel|donkey|mule|fish|carp|crab|shrimp',
}
TAGS = {
 'Four Gentlemen (plum, orchid, bamboo, chrysanthemum)': r'plum|orchid|bamboo|chrysanthem',
 'Pine, rock & old trees': r'\bpine|rock|old tree|cypress|juniper|withered tree',
 'Buddhist': r'buddh|luohan|lohan|arhat|guanyin|bodhisattva|avalokit|monk|chan |zen|sutra|amitabha|maitreya|vimalakirti|bodhidharma|hell|ten kings|temple',
 'Daoist & immortals': r'dao|tao|immortal|xian\b|lü dongbin|zhong kui|star god|longevity|shoulao|queen mother|xiwangmu|elixir|peach',
 'Portraits': r'portrait|likeness',
 'Women': r'lady|ladies|women|woman|beaut|consort|maiden|courtesan|girl|empress',
 'Children': r'child|boy|boys|infant|baby',
 'Scholars & hermits': r'scholar|recluse|hermit|retreat|studio|reading|lofty|sage|poet|literati|visitor|friend|zither|qin\b',
 'Fishermen & boats': r'fisherm|fishing|boat|ferry|angler|oar|sail',
 'Horses': r'horse|steed|groom|stable',
 'Oxen & buffalo': r'\box\b|oxen|buffalo|herd',
 'Monkeys & gibbons': r'monkey|gibbon|ape',
 'Dragons & mythic beasts': r'dragon|qilin|phoenix|lion',
 'Insects': r'insect|butterfl|cicada|dragonfl|cricket|grasshopper|bee\b|mantis',
 'Fish & water creatures': r'fish|carp|crab|shrimp|frog|turtle|tortoise',
 'Fruit & vegetables': r'fruit|vegetable|melon|grape|cabbage|radish|loquat|lychee|persimmon|peach|pomegranate|eggplant|gourd|citron|bamboo shoot',
 'Architecture & palaces': r'palace|pavilion|tower|terrace|hall|temple|bridge|gate|city|building|mansion|villa|ruled-line|jiehua',
 'Gardens': r'garden|courtyard|rockery',
 'Gatherings & elegant pastimes': r'gathering|banquet|party|elegant|music|tea|chess|game|zither|qin\b|incense|wine|drinking|poetry',
 'Narrative & history': r'story|legend|tale|history|scenes from|illustration|odes|ode |classic|biography|exemplary|returning|farewell|lament|rhapsody|fu\b|red cliff|peach blossom spring',
 'Daily life & work': r'farm|farming|weaving|silk|plough|market|pedlar|peddler|vendor|harvest|workmen|labor|village|festival|cart|travelers|merchant',
 'Water, waves & waterfalls': r'water|wave|waterfall|cascade|torrent|rapids|tide|stream|river',
 'Snow & winter': r'snow|winter|frost|ice|cold',
 'Night & moon': r'moon|night|evening|dusk|twilight|lantern|star',
 'Rain, mist & clouds': r'rain|mist|cloud|fog|storm|wind',
 'Birds of prey': r'eagle|hawk|falcon|kite',
 'Cranes': r'crane',
 'Waterbirds': r'duck|goose|geese|egret|heron|mandarin|swan|kingfisher|wild ?geese|reed',
 'Small birds': r'sparrow|magpie|swallow|finch|oriole|thrush|warbler|myna|bulbul|wagtail|white-eye|shrike|starling|bird on',
 'Lotus': r'lotus',
 'Peonies': r'peon',
 'Bamboo': r'bamboo',
 'Plum blossom': r'plum',
 'Orchids': r'orchid',
}
SEASON = {'Spring': r'spring|peach blossom|apricot|willow', 'Summer': r'summer|lotus|heat|shade', 'Autumn': r'autumn|fall\b|chrysanthem|maple|red leaves', 'Winter': r'winter|snow|frost|plum'}

SUBJ_ZH = {'Landscape': '山|水|溪|江|河|湖|峰|巖|岩|瀑|泉|林|雲|煙|嵐|谷|村|景|勝|壑|嶂|石',
 'Bird-and-flower': '花|鳥|禽|梅|竹|蘭|菊|荷|蓮|牡丹|松|鶴|雀|鴨|雁|鷺|鷹|蟲|蝶|果|蔬|卉|枇杷|柳|桃|芙蓉|鵲|鳩',
 'Figure': '人|仕女|美人|羅漢|觀音|佛|仙|高士|翁|嬰|童|像|帝|后|妃|漁|樵|騎|僧|老子|孔子|鍾馗|圖像',
 'Animals': '馬|牛|虎|猫|貓|犬|猴|猿|鹿|鼠|龍|羊|兔|魚|蟹|驢'}
TAGS_ZH = {'Four Gentlemen (plum, orchid, bamboo, chrysanthemum)': '梅|蘭|竹|菊', 'Buddhist': '佛|羅漢|觀音|僧|禪|經|菩薩', 'Daoist & immortals': '仙|道|壽|星|鍾馗',
 'Women': '仕女|美人|妃|女', 'Children': '嬰|童|兒', 'Scholars & hermits': '高士|隱|讀書|書齋|幽居|琴', 'Fishermen & boats': '漁|舟|船|釣', 'Horses': '馬', 'Oxen & buffalo': '牛',
 'Architecture & palaces': '宮|樓|閣|殿|寺|橋|亭|界畫', 'Gardens': '園', 'Snow & winter': '雪|寒|冬', 'Night & moon': '月|夜', 'Rain, mist & clouds': '雨|雲|煙|霧|風',
 'Pine, rock & old trees': '松|石|古木|枯木', 'Lotus': '荷|蓮', 'Peonies': '牡丹', 'Bamboo': '竹', 'Plum blossom': '梅', 'Orchids': '蘭', 'Cranes': '鶴',
 'Fish & water creatures': '魚|蟹|蝦', 'Insects': '蟲|蝶|蟬', 'Monkeys & gibbons': '猴|猿', 'Fruit & vegetables': '果|蔬|瓜|桃|枇杷|荔', 'Waterbirds': '鴨|雁|鷺|鴛|鵝',
 'Water, waves & waterfalls': '瀑|泉|溪|江|波|濤', 'Portraits': '像', 'Dragons & mythic beasts': '龍|鳳'}
SEASON_ZH = {'Spring': '春', 'Summer': '夏', 'Autumn': '秋', 'Winter': '冬|雪'}
def subjects(text):
    g, tags, se = subjects_en(text)
    zh = ''.join(HAN.findall(text or ''))
    if zh:
        g += [k for k, r in SUBJ_ZH.items() if re.search(r, zh) and k not in g]
        tags += [k for k, r in TAGS_ZH.items() if re.search(r, zh) and k not in tags]
        se += [k for k, r in SEASON_ZH.items() if re.search(r, zh) and k not in se]
    return g, tags, se
def subjects_en(text):
    t = (text or '').lower()
    g = [k for k, r in SUBJ.items() if re.search(r, t)]
    # a flower title with a figure word like "man" shouldn't flip; keep all matches but order by priority
    tags = [k for k, r in TAGS.items() if re.search(r, t)]
    se = [k for k, r in SEASON.items() if re.search(r, t)]
    return g, tags, se

# approach (brush mode), by school
APPROACH = {
 'Southern Song Academy': 'Academy / meticulous', 'Song Academy': 'Academy / meticulous', 'Ming court': 'Academy / meticulous',
 'Qing court': 'Academy / meticulous', 'Six Dynasties & Tang masters': 'Academy / meticulous', 'Ningbo Buddhist workshops': 'Academy / meticulous',
 'Yangzhou professionals': 'Academy / meticulous',
 'Chan painting': 'Freehand (xieyi)', 'Yangzhou Eccentrics': 'Freehand (xieyi)', 'Individualists': 'Freehand (xieyi)',
 'Late Ming innovators': 'Literati', 'Shanghai school': 'Freehand (xieyi)', 'Zhe school': 'Bold professional ink',
 'Four Yuan Masters': 'Literati', 'Yuan literati': 'Literati', 'Song literati': 'Literati', 'Wu school': 'Literati',
 'Songjiang school': 'Literati', 'Orthodox school': 'Literati', 'Anhui school': 'Literati', 'Nanjing school': 'Literati',
 'Mid-late Qing': 'Literati', 'Southern Song literati & Chan': 'Literati', 'Northern Song landscape': 'Monumental landscape',
 'Five Dynasties masters': 'Monumental landscape', 'Lingnan precursors': 'Academy / meticulous', 'Jin dynasty': 'Literati',
 'Ming figure painting': 'Academy / meticulous',
}

out = []
def add(**k):
    out.append(k)

def commons_thumb(url, w=480):
    # url like https://upload.wikimedia.org/wikipedia/commons/a/ab/Name.jpg
    p = url.split('/wikipedia/commons/')[1]
    name = p.split('/')[-1]
    if name.lower().endswith(('.tif', '.tiff')):
        return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{p}/lossy-page1-{w}px-{name}.jpg'
    return f'https://upload.wikimedia.org/wikipedia/commons/thumb/{p}/{w}px-{name}'

def finish(rec, artist_text, title, medium_text, date_text, period_text, extra_text=''):
    k = match_artist(artist_text)
    rec['attribution'] = attribution(artist_text)
    if k:
        a = A[k]
        rec['artist'] = a['name']; rec['artistZh'] = a['zh']; rec['artistDates'] = a['dates']; rec['school'] = a['school']
        if rec['attribution'] == 'Unidentified artist': rec['attribution'] = 'After / in the style of'
    else:
        name = re.sub(r'\(.*?\)|\n.*', '', artist_text or '').strip(' ,;|')
        name = re.sub(r'^(Formerly attributed to|Attributed to|After|Style of)\s+', '', name, flags=re.I)
        rec['artist'] = name if name and rec['attribution'] != 'Unidentified artist' else 'Unidentified artist'
        rec['artistZh'] = zh_of(artist_text); rec['artistDates'] = ''; rec['school'] = None
    rec['approach'] = APPROACH.get(rec['school']) if rec['school'] else None
    y1, y2 = parse_years(date_text)
    dy = dyn_from_text(period_text) or dyn_from_text(date_text)
    if dy == 'Song':
        dy = dyn_from_year(((y1 or 960) + (y2 or 1279)) // 2) if y1 else 'Northern Song' if False else 'Song (general)'
    if not dy and y1: dy = dyn_from_year((y1 + y2) // 2)
    if not y1 and dy:
        for a_, b_, n in DYN:
            if n == dy: y1, y2 = int(max(a_, 200)), int(b_)
    rec['dynasty'] = dy or 'Unknown'
    rec['y1'], rec['y2'] = y1, y2
    rec['century'] = century((y1 + y2) // 2) if y1 else None
    rec['format'] = fmt(medium_text + ' ' + rec.get('objectName', ''))
    rec['support'] = support(medium_text)
    rec['palette'] = palette(medium_text, title)
    g, tags, se = subjects(' '.join([title, extra_text]))
    rec['genre'] = g or ['Other']
    rec['tags'] = tags; rec['season'] = se
    rec.pop('objectName', None)
    add(**rec)

# ---------- Met ----------
met = json.load(open('met_objects.json'))
dims = json.load(open('met_dims.json'))
for o in met:
    if not o.get('primaryImage'): continue
    imgs = [o['primaryImage']] + (o.get('additionalImages') or [])
    tags = ' '.join(t['term'] for t in (o.get('tags') or []))
    d = dims.get(o['primaryImage'])
    rec = dict(id=f"met{o['objectID']}", src='Met', museum='The Metropolitan Museum of Art', title=o['title'], titleZh=zh_of(o['title']),
               date=o.get('objectDate', ''), medium=o.get('medium', ''), dims=o.get('dimensions', ''), credit=o.get('creditLine', ''),
               link=o.get('objectURL'), desc='', license='CC0 (Met Open Access)', objectName=o.get('objectName', ''),
               thumb=o.get('primaryImageSmall') or o['primaryImage'],
               images=[{'t': 'img', 'u': u} for u in imgs], px=list(d) if d else None, highlight=bool(o.get('isHighlight')))
    finish(rec, o.get('artistDisplayName', ''), o['title'], o.get('medium', '') + ' ' + o.get('objectName', ''), o.get('objectDate', ''), o.get('period', ''), tags)

# ---------- Cleveland ----------
for a in json.load(open('cma.json'))['data']:
    im = a.get('images') or {}
    if not im.get('print'): continue
    late = a.get('creation_date_latest') or 0
    if late and late > 1912: continue
    cr = a.get('creators') or []
    atext = '; '.join((c.get('description') or '') + ' ' + (c.get('name_in_original_language') or '') for c in cr)
    imgs = [im] + (a.get('alternate_images') or [])
    images = []
    for x in imgs:
        p = x.get('print') or {}
        if p.get('url'): images.append({'t': 'img', 'u': p['url'], 'w': int(p.get('width') or 0), 'h': int(p.get('height') or 0),
                                         'full': (x.get('full') or {}).get('url'), 'fw': int((x.get('full') or {}).get('width') or 0), 'fh': int((x.get('full') or {}).get('height') or 0)})
    f0 = im.get('full') or {}
    rec = dict(id=f"cma{a['id']}", src='Cleveland', museum='Cleveland Museum of Art', title=a['title'], titleZh=a.get('title_in_original_language') or '',
               date=a.get('creation_date', ''), medium=a.get('technique', ''), dims=a.get('measurements', ''), credit=a.get('creditline', ''),
               link=a.get('url'), desc=clean(a.get('description')), didyouknow=clean(a.get('did_you_know')), license='CC0 (Cleveland Open Access)',
               thumb=(im.get('web') or {}).get('url'), images=images, px=[int(f0.get('width') or 0), int(f0.get('height') or 0)] if f0 else None,
               highlight=bool(a.get('is_highlight')), inscription=clean((a.get('inscriptions') or [{}])[0].get('inscription_translation')) if a.get('inscriptions') else '')
    finish(rec, atext, a['title'], a.get('technique', ''), a.get('creation_date', ''), ' '.join(a.get('culture') or []))

# ---------- AIC ----------
for o in json.load(open('aic.json')):
    if not o.get('image_id'): continue
    rec = dict(id=f"aic{o['id']}", src='AIC', museum='Art Institute of Chicago', title=o['title'], titleZh=zh_of(' '.join(o.get('alt_titles') or [])),
               date=o.get('date_display', ''), medium=o.get('medium_display', ''), dims=o.get('dimensions', ''), credit=o.get('credit_line', ''),
               link=f"https://www.artic.edu/artworks/{o['id']}", desc=clean(o.get('description')), license='CC0 image; text CC BY (Art Institute of Chicago)',
               thumb=f"https://www.artic.edu/iiif/2/{o['image_id']}/full/400,/0/default.jpg",
               images=[{'t': 'iiif', 'u': f"https://www.artic.edu/iiif/2/{o['image_id']}"}], px=None)
    finish(rec, o.get('artist_display', ''), o['title'], o.get('medium_display', ''), o.get('date_display', ''), o.get('date_display', ''), ' '.join(o.get('subject_titles') or []))

# ---------- Freer ----------
for r in json.load(open('fsg_cn.json')):
    c = r['content']; ft = c['freetext']; dn = c['descriptiveNonRepeating']
    media = (dn.get('online_media') or {}).get('media') or []
    media = [m for m in media if m.get('idsId') and (m.get('usage') or {}).get('access') == 'CC0']
    if not media: continue
    g = lambda k, lab=None: '; '.join(x['content'] for x in ft.get(k, []) if (lab is None or x['label'] == lab))
    datet = g('date', 'Date'); per = g('date', 'Period')
    med = g('physicalDescription', 'Medium'); dimt = g('physicalDescription', 'Dimensions')
    names = '; '.join(x['content'] for x in ft.get('name', []) if 'artist' in x['label'].lower() or 'painter' in x['label'].lower()); topics = g('topic'); school_note = g('notes', 'School/Tradition')
    title = dn['title']['content']
    images = []
    for m in media:
        res = {x['label']: x for x in m.get('resources', [])}
        hr = res.get('High-resolution JPEG') or {}
        images.append({'t': 'iiif', 'u': f"https://ids.si.edu/ids/iiif/{m['idsId']}", 'w': hr.get('width'), 'h': hr.get('height')})
    hr0 = images[0]
    alt = ' '.join(m.get('altTextAccessibility', '') for m in media[:1])
    rec = dict(objectName=alt, id='fsg' + dn['record_ID'].split('_', 1)[1].replace('.', '_'), src='Freer', museum='National Museum of Asian Art (Freer Gallery), Smithsonian',
               title=title, titleZh=zh_of(title), date=datet, medium=med, dims=dimt, credit=g('creditLine'), link=dn.get('record_link'),
               desc='', license='CC0 (Smithsonian Open Access)', thumb=f"https://ids.si.edu/ids/iiif/{media[0]['idsId']}/full/!400,400/0/default.jpg",
               images=images, px=[hr0['w'], hr0['h']] if hr0.get('w') else None, schoolNote=school_note)
    finish(rec, names, title, med, datet, per, topics)

# ---------- Commons (Wikidata) ----------
cm = json.load(open('commons.json'))
info = cm['info']
WX = json.load(open('wd_extra.json'))
NOCOPY = {'The Palace Museum', 'Shanghai Museum', 'Liaoning Provincial Museum', 'Tianjin Museum', 'National Museum of China', 'Zhejiang Provincial Museum',
          'Nanjing Museum', 'Wulin Academy of Arts', 'Ebara Hatakeyama Museum of Art', 'Nezu Museum', 'Osaka City Museum of Fine Arts', 'Hong Kong Museum of Art',
          'The Chinese University of Hong Kong'}
API_SRC = {'Metropolitan Museum of Art', 'Cleveland Museum of Art', 'Art Institute of Chicago', 'Freer Gallery of Art'}
linkonly = []
for it in cm['items']:
    colls = set(it['colls'])
    if colls & API_SRC: continue
    title = it.get('itemLabel', '')
    if re.fullmatch(r'Q\d+', title): title = it.get('zh', title)
    y = int(it['inception'][:5].lstrip('+').split('-')[0] or 0) if it.get('inception') and it['inception'][0] != 'h' else None
    if y and y > 1912: continue
    datet = str(y) if y else ''
    museum = sorted(colls)[0] if colls else 'Unknown collection'
    wx = WX.get(it['q'], {})
    mat = wx.get('mat', '').replace('|', ' '); gen = wx.get('gen', '').replace('|', ' '); dep = wx.get('dep', '').replace('|', ', ')
    if 'oil' in mat or 'canvas' in mat: continue
    cy = None
    for k in ('floruit', 'born', 'died'):
        if wx.get(k) and wx[k][0] in '+-12':
            try: cy = int(wx[k].lstrip('+')[:4]) + (25 if k == 'born' else -10 if k == 'died' else 0); break
            except: pass
    if not y and cy: y = None; datet = f'artist active c. {cy}'
    if colls & NOCOPY:
        if int(wx.get('sitelinks', 0)) >= 1:
            linkonly.append(dict(q=it['q'], title=title, zh=it.get('zh', ''), creator=it.get('creatorLabel', ''), creatorZh=it.get('creatorZh', ''), museum=museum, y=y or cy,
                                 zhwiki=wx.get('zhwiki'), enwiki=wx.get('enwiki'), sitelinks=int(wx.get('sitelinks', 0))))
        continue
    imgs = [info[f] for f in it['images'] if f in info]
    if not imgs: continue
    ii = imgs[0]
    images = []
    for x in imgs:
        mp = x['width'] * x['height'] / 1e6
        if x['mime'] in ('image/jpeg', 'image/png') and mp <= 45:
            images.append({'t': 'img', 'u': x['url'], 'w': x['width'], 'h': x['height']})
        else:
            images.append({'t': 'big', 'u': x['url'], 'w': x['width'], 'h': x['height'], 'mime': x['mime']})
    lic = (ii.get('extmetadata', {}).get('LicenseShortName') or {}).get('value', '')
    rec = dict(id='wd' + it['q'], src='Commons', museum=museum, title=title, titleZh=it.get('zh', '') if it.get('zh') != title else '',
               date=datet, medium='', dims='', credit='', link=f"https://www.wikidata.org/wiki/{it['q']}", commons=ii.get('descriptionurl'),
               desc='', license=f'{lic} (via Wikimedia Commons)', thumb=commons_thumb(ii['url']), images=images, px=[ii['width'], ii['height']])
    medium = ' '.join(['ink' if 'ink' in (mat + gen) else '', 'and color' if 'color' in gen else '', 'on ' + mat if mat else '']).strip()
    if 'fan' in gen: medium = 'fan; ' + medium
    if 'album' in wx.get('ins', ''): medium = 'album leaf; ' + medium
    rec['medium'] = medium; rec['depicts'] = dep
    finish(rec, (it.get('creatorLabel', '') + ' ' + it.get('creatorZh', '')).strip(), title, medium + ' ' + title, datet, '', dep + ' ' + gen)
    if rec['dynasty'] == 'Unknown' and not y: pass

# ---------- de-duplicate & finalize ----------
seen = set(); final = []
CALLI = re.compile(r'calligraph|^letter$|^letters?\b|尺牘|法書|書帖|^painting$|^album leaf$', re.I)
for r in out:
    if CALLI.search(r['title'].strip()) and not re.search(r'paint|圖|畫', r['title'], re.I): continue
    if r['title'].startswith('Dr. '): continue
    key = (r['src'], r['id'])
    if key in seen: continue
    seen.add(key)
    if r['px'] and r['px'][0]: r['mp'] = round(r['px'][0] * r['px'][1] / 1e6, 1)
    else: r['mp'] = None
    final.append(r)
json.dump(final, open('paintings_raw.json', 'w'), ensure_ascii=False)
for x in linkonly:
    k = match_artist((x.get('creator') or '') + ' ' + (x.get('creatorZh') or '') + ' ' + (x.get('zh') or ''))
    if k: x['creator'] = A[k]['name']; x['creatorZh'] = A[k]['zh']; x['school'] = A[k]['school']
    y = x.get('y'); x['dyn'] = dyn_from_year(y) if y else 'Unknown'
    g, tags, se = subjects((x.get('title') or '') + ' ' + (x.get('zh') or ''))
    x['genre'] = g or ['Other']; x['tags'] = tags; x['season'] = se
    x['century'] = century(y) if y else None
json.dump(linkonly, open('linkonly_raw.json', 'w'), ensure_ascii=False)
print(len(final), collections.Counter(r['src'] for r in final))
print('linkonly', len(linkonly))
print(collections.Counter(r['dynasty'] for r in final))
print(collections.Counter(g for r in final for g in r['genre']))
print(collections.Counter(r['school'] for r in final).most_common(40))
print(collections.Counter(r['attribution'] for r in final))
print(collections.Counter(r['format'] for r in final))
print(collections.Counter(r['support'] for r in final))
