import json,urllib.request,urllib.parse,time
cm=json.load(open('commons.json'))
qs=[it['q'] for it in cm['items']]
UA={'User-Agent':'MiaPaintingCollection/1.0 (personal study)','Accept':'application/sparql-results+json'}
res={}
for i in range(0,len(qs),400):
    vals=' '.join('wd:'+q for q in qs[i:i+400])
    q=f'''SELECT ?item (GROUP_CONCAT(DISTINCT ?matL;separator="|") AS ?mat) (GROUP_CONCAT(DISTINCT ?genL;separator="|") AS ?gen) (GROUP_CONCAT(DISTINCT ?depL;separator="|") AS ?dep) (GROUP_CONCAT(DISTINCT ?insL;separator="|") AS ?ins) (SAMPLE(?b) AS ?born) (SAMPLE(?d) AS ?died) (SAMPLE(?fl) AS ?floruit) (SAMPLE(?sl) AS ?sitelinks) (SAMPLE(?zhw) AS ?zhwiki) (SAMPLE(?enw) AS ?enwiki) (SAMPLE(?dpm) AS ?dpmid) WHERE {{
VALUES ?item {{ {vals} }}
OPTIONAL {{ ?item wdt:P186 ?m. ?m rdfs:label ?matL FILTER(LANG(?matL)="en") }}
OPTIONAL {{ ?item wdt:P136 ?g. ?g rdfs:label ?genL FILTER(LANG(?genL)="en") }}
OPTIONAL {{ ?item wdt:P180 ?dp. ?dp rdfs:label ?depL FILTER(LANG(?depL)="en") }}
OPTIONAL {{ ?item wdt:P31 ?in. ?in rdfs:label ?insL FILTER(LANG(?insL)="en") }}
OPTIONAL {{ ?item wdt:P170 ?c. OPTIONAL {{?c wdt:P569 ?b}} OPTIONAL {{?c wdt:P570 ?d}} OPTIONAL {{?c wdt:P1317 ?fl}} }}
OPTIONAL {{ ?item wikibase:sitelinks ?sl }}
OPTIONAL {{ ?zhw schema:about ?item; schema:isPartOf <https://zh.wikipedia.org/> }}
OPTIONAL {{ ?enw schema:about ?item; schema:isPartOf <https://en.wikipedia.org/> }}
}} GROUP BY ?item'''
    for t in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request('https://query.wikidata.org/sparql',data=urllib.parse.urlencode({'query':q}).encode(),headers=UA),timeout=170));break
        except Exception as e:
            print('retry',e);time.sleep(20)
    for b in r['results']['bindings']:
        res[b['item']['value'].rsplit('/',1)[1]]={k:v['value'] for k,v in b.items() if k!='item'}
    time.sleep(2)
json.dump(res,open('wd_extra.json','w'),ensure_ascii=False);print(len(res))
