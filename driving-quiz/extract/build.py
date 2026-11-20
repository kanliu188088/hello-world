import json,re,sys,pdfplumber,io,base64
rows=json.load(open('rows.json'))
tr=str.maketrans('（）１２３','()123')
isans=lambda s: re.fullmatch(r'\(?[123]\)?',s.translate(tr))
qs=[]
for r in rows:
    c=r['cells']
    if len(c)<3: continue
    num=c[0]
    if re.fullmatch(r'\d+',num):
        rest=c[1:]; a=''
        for i,x in enumerate(rest[:2]):
            if isans(x): a=x; rest=rest[:i]+rest[i+1:]; break
        qs.append(dict(n=int(num),a=a,t=''.join(rest),segs=[(r['page'],r['bbox'])]))
    elif num=='' and qs:
        if ''.join(c)=='案': continue
        qs[-1]['t']+=''.join(c[1:]) ; qs[-1]['segs'].append((r['page'],r['bbox']))
bad=0
for q in qs:
    t=q['t'].translate(tr)
    m=re.fullmatch(r'\(?([123])\)?',q['a'].translate(tr))
    if not m: print('badans',q['n'],q['a'],t); bad+=1; continue
    q['a']=int(m.group(1))
    i1=t.find('(1)'); i2=t.find('(2)',i1+1); i3=t.find('(3)',i2+1)
    if min(i1,i2,i3)<0: print('badopt',q['n'],t); bad+=1; continue
    q['q']=t[:i1].strip(); q['o']=[t[i1+3:i2].strip(),t[i2+3:i3].strip(),t[i3+3:].strip()]
    q['imgopt']=not all(len(o.strip(' 。'))>0 for o in q['o'])
    if '(1)' in t[i1+1:] or '(2)' in t[i2+1:] or '(3)' in t[i3+1:] or '(4)' in t: print('multi',q['n'],t)
print('bad',bad)
# images
pdf=pdfplumber.open(sys.argv[1])
imgs={}
nimg=0;tot=0
for pi,page in enumerate(pdf.pages):
    pq=[(q,bb) for q in qs for (p,bb) in q['segs'] if p==pi+1 and bb[0]<100]  # main rows only
    for q,bb in pq:
        ims=[im for im in page.images if im['top']>=bb[1]-2 and im['bottom']<=bb[3]+2]
        if not ims: continue
        if q['imgopt'] or '圖1' in q['t']:
            ws=[w for w in page.crop((bb[0],bb[1],bb[2],bb[3])).extract_words() if w['x0']>100 and not re.fullmatch(r'[(（]?[123１２３][)）]?',w['text']) or w['x0']>150]
            x0=min([w['x0'] for w in ws]+[i['x0'] for i in ims])-3
            box=(x0,bb[1]+2,bb[2]-2,bb[3]-2); full=True
        else:
            box=(min(i['x0'] for i in ims)-2,min(i['top'] for i in ims)-2,max(i['x1'] for i in ims)+2,max(i['bottom'] for i in ims)+2); full=False
        box=(max(box[0],0),max(box[1],0),min(box[2],page.width),min(box[3],page.height))
        im=page.crop(box).to_image(resolution=200 if not full else 170).original.convert('RGB')
        if full:
            from PIL import ImageChops,Image
            g=im.convert('L').point(lambda v:255 if v<200 else 0); bx=g.getbbox()
            if bx: im=im.crop((max(bx[0]-8,0),max(bx[1]-8,0),min(bx[2]+8,im.width),min(bx[3]+8,im.height)))
        b=io.BytesIO(); im.save(b,'WEBP',quality=80)
        if q['n'] in imgs: print('dupimg',q['n'])
        imgs[q['n']]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode(); q['full']=full
        tot+=len(b.getvalue())
print(len(imgs),'imgs',tot)
for q in qs:
    if q['imgopt'] and q['n'] not in imgs: print('imgopt w/o image',q['n'],q['t'])
    if not q['q'] and q['n'] not in imgs: print('no stem no img',q['n'],q['t'])
out=[]
for q in qs:
    d=dict(n=q['n'],a=q['a'],q=re.sub(r'^圖1 ?圖2 ?圖3','',q['q']),o=[o if o.strip(' 。') else '' for o in q['o']])
    if q['n'] in imgs: d['i']=2 if q.get('full') else 1
    out.append(d)
open(sys.argv[2]+'/questions.json','w').write('[\n'+',\n'.join(json.dumps(d,ensure_ascii=False,separators=(',',':')) for d in out)+'\n]\n')
open(sys.argv[2]+'/images.json','w').write(json.dumps({str(k):v for k,v in imgs.items()}))
import collections
print(collections.Counter(q['a'] for q in qs))
