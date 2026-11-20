import json,urllib.request,urllib.parse,time,collections
d=json.load(open('wd2.json'))['results']['bindings']
NOCOPY={'The Palace Museum','Shanghai Museum','Liaoning Provincial Museum','Tianjin Museum','National Museum of China','Zhejiang Provincial Museum','Nanjing Museum','Wulin Academy of Arts','Ebara Hatakeyama Museum of Art','Nezu Museum','Osaka City Museum of Fine Arts','Hong Kong Museum of Art','The Chinese University of Hong Kong','Hubei Provincial Museum','Hunan Provincial Museum','Jilin Provincial Museum','Sichuan Museum','Guangdong Museum','Shandong Museum','Henan Museum','Shaanxi History Museum','Capital Museum','Suzhou Museum','Anhui Museum','Yunnan Provincial Museum'}
API_SRC={'Metropolitan Museum of Art','Cleveland Museum of Art','Art Institute of Chicago','Freer Gallery of Art'}
items=collections.OrderedDict()
for b in d:
    q=b['item']['value'].rsplit('/',1)[1]
    it=items.setdefault(q,{'q':q,'colls':set(),'images':[]})
    for k in ('itemLabel','zh','creatorLabel','creatorZh','inception'):
        if k in b: it[k]=b[k]['value']
    if 'creator' in b: it['creatorQ']=b['creator']['value'].rsplit('/',1)[1]
    if 'collLabel' in b: it['colls'].add(b['collLabel']['value'])
    f=urllib.parse.unquote(b['image']['value'].rsplit('/',1)[1])
    if f not in it['images']: it['images'].append(f)
for it in items.values(): it['colls']=sorted(it['colls'])
print(len(items))
want=[it for it in items.values() if not (set(it['colls'])&NOCOPY) and not (set(it['colls'])&API_SRC)]
print('commons-needed',len(want))
files=sorted({f for it in want for f in it['images']})
info={}
UA={'User-Agent':'MiaPaintingCollection/1.0 (https://github.com/miapritchina; personal study)'}
for i in range(0,len(files),50):
    ch=files[i:i+50]
    q=urllib.parse.urlencode({'action':'query','titles':'|'.join('File:'+f for f in ch),'prop':'imageinfo','iiprop':'url|size|mime|extmetadata','iiextmetadatafilter':'LicenseShortName|Artist','format':'json'})
    for t in range(5):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+q,headers=UA),timeout=60));break
        except Exception as e: time.sleep(10*(t+1))
    norm={n['to']:n['from'] for n in r['query'].get('normalized',[])}
    for p in r['query']['pages'].values():
        if 'imageinfo' in p:
            ii=p['imageinfo'][0]; info[p['title'][5:]]=ii
    time.sleep(1.5)
json.dump({'items':list(items.values()),'info':info},open('commons.json','w'),ensure_ascii=False)
print(len(files),len(info))
