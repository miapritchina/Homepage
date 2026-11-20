import os, math, re, pyvips, xml.etree.ElementTree as ET
T='/home/claude/homepage/chinese-paintings/tiles'
for f in sorted(os.listdir(T)):
    if not f.endswith('.dzi'): continue
    key=f[:-4]; base=f'{T}/{key}_files'
    if os.path.exists(f'{base}/.fixed'): continue
    r=ET.parse(f'{T}/{f}').getroot(); s=r.find('{*}Size'); W=int(s.get('Width')); H=int(s.get('Height'))
    maxL=math.ceil(math.log2(max(W,H)))
    lv=sorted(int(x) for x in os.listdir(base) if x.isdigit())
    if lv[-1]==maxL and lv[0]==0: open(f'{base}/.fixed','w').close(); continue
    shift=maxL-lv[-1]
    for k in reversed(lv): os.rename(f'{base}/{k}', f'{base}/{k+shift}.tmp')
    for k in lv: os.rename(f'{base}/{k+shift}.tmp', f'{base}/{k+shift}')
    low=lv[0]+shift
    im=pyvips.Image.new_from_file(f'{base}/{low}/0_0.jpg')
    for L in range(low-1,-1,-1):
        w=max(1,math.ceil(W/2**(maxL-L))); h=max(1,math.ceil(H/2**(maxL-L)))
        im=im.thumbnail_image(w,height=h,size='force')
        os.makedirs(f'{base}/{L}',exist_ok=True); im.write_to_file(f'{base}/{L}/0_0.jpg[Q=80]')
    if os.path.exists(f'{base}/vips-properties.xml'): os.remove(f'{base}/vips-properties.xml')
    open(f'{base}/.fixed','w').close(); print('fixed',key,maxL,shift)
