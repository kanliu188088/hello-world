import pdfplumber, json, re, sys
pdf = pdfplumber.open(sys.argv[1])
rows=[]  # dict(num, ans, text, page, top, bottom)
section=None
for pi,page in enumerate(pdf.pages):
    imgs=[(im['top'],im['bottom'],im['x0'],im['x1']) for im in page.images]
    for t in page.find_tables():
        data=t.extract()
        for r,cells in zip(t.rows,data):
            cells=[(c or '').replace('\n','').strip() for c in cells]
            top,bottom=r.bbox[1],r.bbox[3]
            if '題號' in cells[0] or (len(cells)>1 and '題' in cells[-1] and '目' in cells[-1] and len(cells[-1])<8): continue
            rows.append(dict(page=pi+1,top=top,bottom=bottom,cells=cells,bbox=r.bbox))
json.dump(rows,open('rows.json','w'),ensure_ascii=False)
print(len(rows))
from collections import Counter
print(Counter(len(r['cells']) for r in rows))
for r in rows[:14]+rows[117:122]: print(r['page'],round(r['top']),r['cells'])
