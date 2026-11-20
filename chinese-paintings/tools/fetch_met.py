import json,sys,concurrent.futures as cf,urllib.request,pandas as pd,time
m=pd.read_csv('met_cn.csv',low_memory=False)
ids=m['Object ID'].tolist()
def get(i):
    for t in range(4):
        try:
            with urllib.request.urlopen(f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{i}',timeout=30) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2+t*3)
    return {'objectID':i,'error':True}
out=[]
with cf.ThreadPoolExecutor(8) as ex:
    for d in ex.map(get,ids): out.append(d)
json.dump(out,open('met_objects.json','w'))
print(len(out),sum(1 for d in out if d.get('primaryImage')))
