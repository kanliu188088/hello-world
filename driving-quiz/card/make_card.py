import qrcode, sys
from PIL import Image, ImageDraw, ImageFont
SITE='https://kanliu188088.github.io/hello-world/driving-quiz/'
URL=SITE+'?openExternalBrowser=1'  # makes LINE open the phone's own browser
W,H=1240,1748  # A6 at 300 dpi
BLUE=(11,78,162); INK=(23,33,46); MUTED=(91,104,120); SOFT=(227,237,250)
F=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',s)
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,430),fill=BLUE)
d.text((W/2,120),'屏東基督教醫院　敬贈',font=F(54),fill=(255,226,122),anchor='mm')
d.text((W/2,225),'汽車駕照筆試',font=F(104),fill='white',anchor='mm')
d.text((W/2,345),'線上練習　1090 題',font=F(72),fill='white',anchor='mm')
qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=10,border=4); qr.add_data(URL); qr.make(fit=True)
q=qr.make_image(fill_color='black',back_color='white').convert('RGB'); Q=640; q=q.resize((Q,Q),Image.NEAREST)
im.paste(q,((W-Q)//2,470)); q.save('qr.png')
d.text((W/2,1140),'用手機「相機」掃描，馬上開始',font=F(56),fill=INK,anchor='mm')
d.text((W/2,1205),'免費・不用安裝・請用 Safari 或 Chrome 開啟',font=F(34),fill=MUTED,anchor='mm')
items=['一題一題用中文念給你聽','圖形題有語音說明','可以顯示越南文對照','模擬考試，馬上知道分數']
y=1280
for t in items:
    d.rounded_rectangle((150,y,W-150,y+78),radius=16,fill=SOFT)
    d.ellipse((176,y+21,212,y+57),fill=BLUE); d.text((240,y+39),t,font=F(42),fill=INK,anchor='lm'); y+=92
d.text((W/2,H-62),'題庫版本 115.5.29　考試內容以監理機關公告為準',font=F(26),fill=MUTED,anchor='mm')
d.text((W/2,H-26),SITE,font=F(22),fill=MUTED,anchor='mm')
im.save('qr-card.png',dpi=(300,300))
# A4 sheet with four cards and cut marks
A=Image.new('RGB',(2480,3508),'white'); ad=ImageDraw.Draw(A)
for i,(x,y) in enumerate([(0,6),(1240,6),(0,1754),(1240,1754)]): A.paste(im,(x,y))
ad.line((1240,0,1240,3508),fill=(200,200,200),width=2); ad.line((0,1754,2480,1754),fill=(200,200,200),width=2)
A.save('qr-card-A4x4.pdf',resolution=300); im.save('qr-card.pdf',resolution=300)
