import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; BG=(253,248,238); INK=(20,20,22); RED=(178,34,34); NAVY=(18,42,84); CREAM=(245,235,214); GREEN=(0,120,60); BLUE=(20,80,180); SLATE=(70,90,110); ORANGE=(200,90,0); GOLD=(176,132,0)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def wrap(t,f,mw,d):
    words=t.split(); lines=[]; cur=""
    for w in words:
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def txt(d,x,y,t,f,fill=INK):
    d.text((x,y),t,font=f,fill=fill); return d.textlength(t,font=f)
def chip(d,x,y,label):
    c={"CONFIRMED":GREEN,"OFFICIAL":BLUE,"REPORTED":SLATE,"CLAIM":ORANGE}.get(label,SLATE); f=F(SANSB,8); w=d.textlength(label,font=f)+8; d.rounded_rectangle([x,y,x+w,y+11],radius=2,fill=c); d.text((x+4,y+1),label,font=f,fill=(255,255,255)); return w
CONT=[ [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,70),(-75,72),(-65,60),(-55,52),(-60,47),(-70,42),(-75,35),(-80,26),(-85,30),(-90,21),(-95,19),(-105,20),(-115,28),(-125,40),(-125,49),(-140,60),(-165,60)], [(-80,10),(-75,5),(-60,5),(-50,0),(-35,-8),(-40,-20),(-48,-28),(-58,-35),(-65,-45),(-70,-55),(-73,-40),(-73,-20),(-80,-5)], [(-10,36),(-9,43),(-2,48),(0,50),(5,58),(10,59),(18,56),(23,60),(30,70),(40,68),(45,60),(35,55),(28,45),(23,40),(19,42),(12,44),(3,43),(-2,37)], [(-6,35),(10,37),(20,32),(32,31),(35,28),(43,12),(51,11),(48,0),(40,-10),(35,-20),(32,-29),(20,-35),(15,-27),(12,-18),(9,4),(-8,5),(-15,12),(-17,15)], [(40,68),(60,70),(80,73),(100,77),(120,73),(140,72),(160,70),(178,66),(170,60),(162,56),(158,52),(142,50),(140,40),(135,35),(130,33),(127,35),(122,38),(120,30),(115,22),(108,18),(105,10),(100,8),(97,15),(92,21),(88,22),(80,13),(77,8),(72,20),(66,25),(60,25),(55,26),(50,29),(48,30),(43,28),(40,36),(36,36),(35,42)], [(113,-22),(114,-30),(115,-35),(124,-33),(130,-32),(137,-35),(140,-38),(147,-39),(150,-37),(153,-27),(146,-19),(142,-11),(136,-12),(132,-12),(126,-14),(122,-17),(118,-20)] ]
HEROES=[ (1,"RIYADH","MIDDLE EAST","CONFIRMED","Houthi drone hits Riyadh's tallest tower again, 11 hurt","A Houthi drone hit the PIF tower, Riyadh's tallest, for the second time in a week. At least 11 hurt: 2 Saudi, 2 Indian, 3 Nepali and 4 Egyptian.","tower","11"), (2,"SHANGHAI","ASIA","OFFICIAL","China probes Shanghai party chief Chen Jining","Chen Jining, 62, faces a probe for serious violations. He is the fourth Politburo member to fall in a probe this year.","gate","62"), (3,"NEW YORK","US / TECH","CONFIRMED","Huawei guilty on 10 of 12 counts","A US jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud. Sentencing is set for September 2027.","court","10/12") ]
CARDS=[ (4,"ZAPORIZHZHIA","EUROPE / WAR","REPORTED","Russian attacks kill 9 across Ukraine in a day","Nine killed, 81 wounded; 96 drones launched, 73 down.","war","Kyiv"), (5,"CAS","AFRICA / SPORT","OFFICIAL","CAS hands Senegal back the AFCON title","Morocco forfeited 3-0; Senegal won 1-0 and took the title.","trophy","CAS"), (6,"HORMUZ","MIDDLE EAST","REPORTED","IRGC attacks container ship in Hormuz","A ship was attacked at 18:58 UTC north of Khasab.","ship","UKMTO"), (7,"NEW YORK","WORLD / MARKETS","CONFIRMED","Dow closes above 50,000 for the first time","Dow closed at 50,018; Taiex set a record, up 8.99%.","chart","Market close"), (8,"REDMOND","WORLD / TECH","REPORTED","Microsoft declares 'Code Red' after historic outage","After a 24-hour outage, Microsoft set a one-hour target.","data","Reuters"), (9,"ESKISEHIR","EUROPE","REPORTED","Turkish military helicopter crash kills 5","An AS-532 crashed in Eskisehir, killing five.","heli","Turkish officials"), (10,"CARTAGENA","AMERICAS","REPORTED","Supermarket hostages: 25 held in Cartagena","Twenty-five held; five elderly women freed.","market","Colombia"), (11,"ADEN","MIDDLE EAST","REPORTED","Houthis advance within 60 km of Aden","Houthi forces advanced to within 60 km of Aden at 16:51 UTC.","desert","Wires"), (12,"LAHJ","MIDDLE EAST","REPORTED","Saudi strikes kill 25, wound 6 in Yemen","Strikes in Wadi Maabaq left 25 dead or missing, six wounded.","strike","Yemen"), (13,"JIUQUAN","WORLD / SPACE","OFFICIAL","China names first foreign astronaut for Tiangong","Tang Hongbo, Wu Yi and Zeeshan Ali of Pakistan were named.","rocket","CMSA") ]
ALSO=[ (14,"Ankara","Haftar visits Turkey for the first time.","REPORTED"),(15,"London","UK sanctions Houthis and 4 officials.","OFFICIAL"),(16,"Villavicencio","Car bomb injures 23.","REPORTED"),(17,"Gaza","Israel kills Hamas internal security chief.","REPORTED"),(18,"Baghdad","Iraq orders control of Kurdish oilfields.","OFFICIAL"),(19,"Gaza","Meningitis alert: 272 cases in October.","OFFICIAL"),(20,"DR Congo","Missing Cessna 208, rebels claim shootdown.","CLAIM"),(21,"Hanoi","Hot-pot explosion kills at least 6.","REPORTED"),(22,"Gulf of Finland","Ukraine hits Russian ship Sparta II.","REPORTED"),(23,"Kuala Lumpur","Myanmar migrant returns planned.","OFFICIAL"),(24,"Ulleungdo","Korea shelter order; Russian jets in ADIZ.","OFFICIAL"),(25,"Dhaka","Hasina plans return on 16 Dec.","REPORTED"),(26,"The Hague","14 nations endorse ICJ Myanmar ruling.","REPORTED"),(27,"Jakarta","Indonesia nominates 2 vice-president candidates.","OFFICIAL"),(28,"Beijing","China sentences Ma to death for spying.","OFFICIAL"),(29,"Brussels","NATO vows defence against space threat.","OFFICIAL"),(30,"Mexico City","US drone aided capture of El Chapo Isidro, arrested Fri 20 Nov.","REPORTED"),(31,"San Salvador","Bukele names 3 soldiers killed in Haiti.","OFFICIAL"),(32,"Ottawa","Pentagon rebukes Canada: only 41.9% of air fleet ready.","REPORTED"),(33,"Washington","US adds Megaspeed to trade blacklist.","OFFICIAL"),(34,"Kyiv","Zelensky urges Ukraine, Russia, US and Europe talks soon.","REPORTED"),(35,"Ras Al Khaimah","UAE bus-truck crash kills 13.","REPORTED"),(36,"London","England record 5,258 heat deaths in summer 2026.","OFFICIAL"),(37,"Kourou","Ariane 6 lofts 36 Amazon satellites.","OFFICIAL"),(38,"Cikande","Factory-fire toll rises to 26.","REPORTED") ]
PINS={1:(24.7,46.7),2:(31.2,121.5),3:(40.7,-74.0),4:(47.8,35.2),5:(14.7,-17.4),6:(26.5,56.3),7:(40.7,-74.0),8:(47.67,-122.12),9:(39.78,30.52),10:(10.39,-75.51),11:(12.79,45.03),12:(13.05,44.88),13:(39.7,98.5)}
LEGEND=["1 Riyadh tower","2 Shanghai probe","3 Huawei verdict","4 Ukraine attacks","5 Senegal title","6 Hormuz ship","7 Dow 50,018","8 Code Red","9 Helicopter crash","10 Cartagena hostages","11 Aden advance","12 Yemen strikes","13 Tiangong crew"]
NUMBERS=[("11","hurt in Riyadh"),("9","killed in Ukraine"),("50,018","Dow close"),("+8.99%","Taiex record"),("25","killed in Yemen"),("26","Cikande toll"),("10/12","Huawei counts"),("96","drones over Ukraine")]
UTC=[("02:15","NATO space defence"),("08:16","Hanoi blast"),("10:42","Saudi strikes"),("14:27","Riyadh tower hit"),("16:51","Houthis near Aden"),("18:58","Hormuz attack"),("20:41","Huawei guilty")]

def scene(d,x,y,w,h,kind,big=""):
    d.rectangle([x,y,x+w,y+h],fill=(16,24,54) if kind in("tower","war","court") else (30,60,90) if kind in("ship","chart","data") else (120,60,30) if kind in("desert","strike") else (20,50,40) if kind=="gate" else (40,40,70))
    if kind=="tower":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(40,40,50)); d.polygon([(x+w*0.42,y+h*0.08),(x+w*0.58,y+h*0.08),(x+w*0.55,y+h*0.55),(x+w*0.45,y+h*0.55)],fill=(200,200,220)); d.polygon([(x+w*0.62,y+h*0.30),(x+w*0.78,y+h*0.30),(x+w*0.75,y+h*0.55),(x+w*0.65,y+h*0.55)],fill=(150,150,175)); d.ellipse([x+w*0.60,y+h*0.02,x+w*0.86,y+h*0.28],fill=(255,120,40)); d.ellipse([x+w*0.68,y+h*0.10,x+w*0.78,y+h*0.20],fill=(255,200,80)); d.ellipse([x+w*0.15,y+h*0.18,x+w*0.22,y+h*0.25],fill=(255,255,255)); d.ellipse([x+w*0.85,y+h*0.12,x+w*0.90,y+h*0.17],fill=(255,255,255))
    elif kind=="gate":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(90,30,30)); d.rectangle([x+w*0.30,y+h*0.18,x+w*0.70,y+h*0.62],fill=(150,40,40)); d.rectangle([x+w*0.38,y+h*0.32,x+w*0.62,y+h*0.62],fill=(30,10,10)); d.polygon([(x+w*0.28,y+h*0.18),(x+w*0.72,y+h*0.18),(x+w*0.66,y+h*0.08),(x+w*0.34,y+h*0.08)],fill=(176,132,0)); d.rectangle([x+w*0.05,y+h*0.40,x+w*0.18,y+h*0.55],fill=(230,230,230)); d.rectangle([x+w*0.82,y+h*0.40,x+w*0.95,y+h*0.55],fill=(230,230,230))
    elif kind=="court":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(60,50,40)); d.polygon([(x+w*0.30,y+h*0.15),(x+w*0.70,y+h*0.15),(x+w*0.62,y+h*0.28),(x+w*0.38,y+h*0.28)],fill=(200,190,170)); d.rectangle([x+w*0.46,y+h*0.28,x+w*0.54,y+h*0.58],fill=(180,170,150)); d.rectangle([x+w*0.10,y+h*0.42,x+w*0.30,y+h*0.58],fill=(120,110,100)); d.rectangle([x+w*0.70,y+h*0.42,x+w*0.90,y+h*0.58],fill=(120,110,100)); d.rectangle([x+w*0.55,y+h*0.35,x+w*0.88,y+h*0.48],fill=(220,60,60))
    elif kind=="war":
        d.rectangle([x,y+h*0.6,x+w,y+h],fill=(30,30,35)); d.polygon([(x+w*0.10,y+h*0.6),(x+w*0.30,y+h*0.25),(x+w*0.50,y+h*0.6)],fill=(70,70,80)); d.polygon([(x+w*0.45,y+h*0.6),(x+w*0.65,y+h*0.30),(x+w*0.85,y+h*0.6)],fill=(55,55,65)); d.ellipse([x+w*0.70,y+h*0.05,x+w*0.90,y+h*0.25],fill=(255,150,50)); d.ellipse([x+w*0.76,y+h*0.11,x+w*0.84,y+h*0.19],fill=(255,220,100)); d.ellipse([x+w*0.20,y+h*0.10,x+w*0.26,y+h*0.16],fill=(255,255,255))
    elif kind=="trophy":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(20,90,50)); d.ellipse([x+w*0.40,y+h*0.10,x+w*0.60,y+h*0.45],fill=(255,210,60)); d.rectangle([x+w*0.45,y+h*0.45,x+w*0.55,y+h*0.62],fill=(200,160,40)); d.rectangle([x+w*0.20,y+h*0.30,x+w*0.35,y+h*0.55],fill=(0,120,60)); d.rectangle([x+w*0.65,y+h*0.30,x+w*0.80,y+h*0.55],fill=(200,40,40))
    elif kind=="ship":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(25,70,110)); d.rectangle([x+w*0.10,y+h*0.38,x+w*0.90,y+h*0.58],fill=(180,60,40)); d.rectangle([x+w*0.15,y+h*0.28,x+w*0.35,y+h*0.38],fill=(230,230,230)); d.rectangle([x+w*0.40,y+h*0.22,x+w*0.60,y+h*0.38],fill=(200,200,200)); d.line([x+w*0.60,y+h*0.22,x+w*0.75,y+h*0.05],fill=(255,255,255),width=2); d.ellipse([x+w*0.78,y+h*0.08,x+w*0.88,y+h*0.18],fill=(255,120,40))
    elif kind=="chart":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(20,40,30)); d.line([x+w*0.05,y+h*0.80,x+w*0.30,y+h*0.70,x+w*0.55,y+h*0.55,x+w*0.80,y+h*0.30,x+w*0.95,y+h*0.12],fill=(80,220,120),width=4); d.line([x,y+h*0.55,x+w,y+h*0.55],fill=(255,80,80),width=2); d.ellipse([x+w*0.88,y+h*0.05,x+w*0.95,y+h*0.12],fill=(255,255,255))
    elif kind=="data":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(50,10,10)); d.rectangle([x+w*0.08,y+h*0.15,x+w*0.30,y+h*0.55],fill=(30,30,40)); d.rectangle([x+w*0.36,y+h*0.15,x+w*0.58,y+h*0.55],fill=(30,30,40)); d.rectangle([x+w*0.64,y+h*0.15,x+w*0.86,y+h*0.55],fill=(30,30,40)); d.rectangle([x+w*0.10,y+h*0.20,x+w*0.28,y+h*0.28],fill=(255,60,60)); d.rectangle([x+w*0.38,y+h*0.20,x+w*0.56,y+h*0.28],fill=(255,60,60)); d.rectangle([x+w*0.66,y+h*0.20,x+w*0.84,y+h*0.28],fill=(255,60,60))
    elif kind=="heli":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(50,60,50)); d.polygon([(x+w*0.10,y+h*0.55),(x+w*0.30,y+h*0.40),(x+w*0.55,y+h*0.55)],fill=(70,80,70)); d.ellipse([x+w*0.25,y+h*0.28,x+w*0.55,y+h*0.50],fill=(90,100,90)); d.rectangle([x+w*0.55,y+h*0.35,x+w*0.90,y+h*0.42],fill=(90,100,90)); d.line([x+w*0.15,y+h*0.28,x+w*0.65,y+h*0.28],fill=(200,200,200),width=3)
    elif kind=="market":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(90,60,20)); d.rectangle([x+w*0.08,y+h*0.20,x+w*0.92,y+h*0.60],fill=(220,180,120)); d.rectangle([x+w*0.15,y+h*0.30,x+w*0.30,y+h*0.50],fill=(200,60,60)); d.rectangle([x+w*0.38,y+h*0.30,x+w*0.53,y+h*0.50],fill=(60,120,200)); d.rectangle([x+w*0.61,y+h*0.30,x+w*0.76,y+h*0.50],fill=(40,140,80))
    elif kind=="desert":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(210,170,90)); d.polygon([(x,y+h*0.55),(x+w*0.35,y+h*0.30),(x+w*0.70,y+h*0.55)],fill=(190,150,70)); d.ellipse([x+w*0.75,y+h*0.08,x+w*0.92,y+h*0.25],fill=(255,220,120)); d.line([x+w*0.10,y+h*0.45,x+w*0.30,y+h*0.45,x+w*0.45,y+h*0.40],fill=(120,80,30),width=3)
    elif kind=="strike":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(60,50,40)); d.rectangle([x+w*0.10,y+h*0.35,x+w*0.55,y+h*0.58],fill=(200,80,30)); d.rectangle([x+w*0.60,y+h*0.42,x+w*0.90,y+h*0.58],fill=(150,60,30)); d.ellipse([x+w*0.70,y+h*0.08,x+w*0.92,y+h*0.30],fill=(255,150,50)); d.ellipse([x+w*0.76,y+h*0.14,x+w*0.86,y+h*0.24],fill=(255,220,100))
    elif kind=="rocket":
        d.rectangle([x,y+h*0.55,x+w,y+h],fill=(40,40,60)); d.polygon([(x+w*0.45,y+h*0.05),(x+w*0.55,y+h*0.05),(x+w*0.58,y+h*0.45),(x+w*0.42,y+h*0.45)],fill=(230,230,240)); d.polygon([(x+w*0.45,y+h*0.05),(x+w*0.55,y+h*0.05),(x+w*0.50,y+h*0.00)],fill=(220,60,60)); d.ellipse([x+w*0.44,y+h*0.45,x+w*0.56,y+h*0.62],fill=(255,180,60)); d.ellipse([x+w*0.70,y+h*0.10,x+w*0.90,y+h*0.30],fill=(200,200,220)); d.ellipse([x+w*0.12,y+h*0.12,x+w*0.22,y+h*0.22],fill=(255,255,255))
    if big:
        f=F(SANSB,44 if w>250 else 20); tw=d.textlength(big,font=f); bx=x+w-tw-8; by=y+4; d.text((bx+2,by+2),big,font=f,fill=(0,0,0)); d.text((bx,by),big,font=f,fill=(255,215,0))
def proj(lon,lat,bx,by,bw,bh):
    return (bx+(lon+170)/360*bw, by+(75-lat)/135*bh)
def draw_map(d,bx,by,bw,bh):
    d.rectangle([bx,by,bx+bw,by+bh],fill=(190,220,235)); d.rectangle([bx,by,bx+bw,by+bh],outline=NAVY,width=1)
    for poly in CONT:
        pts=[proj(lon,lat,bx,by,bw,bh) for lon,lat in poly]; d.polygon(pts,fill=(170,200,140),outline=(60,90,60))
    off={7:(14,-12),12:(16,10),3:(-16,-12)}
    for n,(lat,lon) in PINS.items():
        px,py=proj(lon,lat,bx,by,bw,bh); dx,dy=off.get(n,(0,0)); qx,qy=px+dx,py+dy
        if (dx,dy)!=(0,0): d.line([px,py,qx,qy],fill=RED,width=1)
        d.ellipse([qx-8,qy-8,qx+8,qy+8],fill=RED,outline=(255,255,255),width=1); f=F(SANSB,9); t=str(n); d.text((qx-d.textlength(t,font=f)/2,qy-5),t,font=f,fill=(255,255,255))

def main():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im); HSRC={1:"Saudi officials",2:"CCDI",3:"US court"}
    d.rectangle([0,0,W,4],fill=RED); txt(d,12,8,"THE WORLD ON ONE DAY",F(SANSB,11),RED); r="38 STORIES \u00b7 6 REGIONS \u00b7 13 FIELDS"; txt(d,W-12-d.textlength(r,font=F(SANSB,11)),8,r,F(SANSB,11))
    txt(d,12,20,"Tuesday 24 November 2026",F(SERIF,30)); txt(d,12,54,"Riyadh tower hit again  \u00b7  Shanghai party chief probed  \u00b7  Huawei guilty on 10 of 12 counts",F(SANS,12),RED)
    segs=[("Europe 9",9,(178,34,34)),("Middle East 8",8,(200,90,0)),("Asia 8",8,(20,80,180)),("Africa 2",2,(0,120,60)),("Americas 7",7,(90,60,140)),("World / Space 4",4,(70,90,110))]; x=12
    for label,n,c in segs:
        w=int(n/38*1000); d.rectangle([x,70,x+w,90],fill=c); f=F(SANSB,9); d.text((x+w/2-d.textlength(label,font=f)/2,75),label,font=f,fill=(255,255,255)); x+=w
    u="  \u00b7  ".join(f"{t}  {s}" for t,s in UTC); txt(d,12,94,u,F(SANSB,10),NAVY)
    x=12
    for num,lab in NUMBERS:
        f=F(SANSB,20); d.text((x+62-d.textlength(num,font=f)/2,110),num,font=f,fill=RED); g=F(SANS,8); d.text((x+62-d.textlength(lab,font=g)/2,132),lab,font=g,fill=INK); x+=125
    d.line([12,146,1012,146],fill=NAVY,width=2)
    for i,(n,place,reg,chipL,head,deck,kind,big) in enumerate(HEROES):
        x=12+i*336; d.rectangle([x,150,x+328,338],outline=NAVY,width=1); scene(d,x,150,328,88,kind,big)
        txt(d,x+6,241,f"{n}  {place} \u00b7 {reg}",F(SANSB,10)); cw=chip(d,x+6,254,chipL); txt(d,x+10+cw,255,f"({HSRC[n]})",F(SANS,8),SLATE); yy=269
        for ln in wrap(head,F(SANSB,13),316,d)[:2]:
            txt(d,x+6,yy,ln,F(SANSB,13),NAVY); yy+=16
        yy=301
        for ln in wrap(deck,F(SANS,10),316,d)[:3]:
            txt(d,x+6,yy,ln,F(SANS,10)); yy+=12
    for i,(n,place,reg,chipL,head,deck,kind,src) in enumerate(CARDS):
        row=i//5; col=i%5; x=12+col*201; y=342+row*111; d.rectangle([x,y,x+193,y+111],outline=NAVY,width=1); scene(d,x,y,193,45,kind,"")
        txt(d,x+5,y+48,f"{n} {place}",F(SANSB,9)); chip(d,x+120,y+48,chipL); yy=y+61
        for ln in wrap(head,F(SANSB,11),183,d)[:2]:
            txt(d,x+5,yy,ln,F(SANSB,11),NAVY); yy+=12
        yy=y+86
        for ln in wrap(deck+" ("+src+")",F(SANS,9),183,d)[:2]:
            txt(d,x+5,yy,ln,F(SANS,9)); yy+=11
    txt(d,12,572,"WORLD MAP \u2014 13 ILLUSTRATED STORIES, NUMBERED 1\u201313",F(SANSB,11),NAVY); draw_map(d,12,588,648,120)
    for i,leg in enumerate(LEGEND):
        lx=672+(i//7)*170; ly=588+(i%7)*18; f=F(SANSB,9); d.ellipse([lx,ly+1,lx+12,ly+13],fill=RED); t=str(i+1); d.text((lx+6-d.textlength(t,font=f)/2,ly+2),t,font=f,fill=(255,255,255)); txt(d,lx+16,ly+1,leg,F(SANS,9))
    txt(d,12,712,"ALSO ON TUESDAY \u2014 25 MORE STORIES",F(SANSB,11),NAVY)
    for col in range(3):
        x=12+col*338; y=728
        for (n,place,head,chipL) in ALSO[col*9:(col+1)*9]:
            for ln in wrap(f"{n} {place}: {head} [{chipL}]",F(SANS,9),326,d):
                txt(d,x,y,ln,F(SANS,9)); y+=11
            y+=9
    d.rectangle([12,932,1012,970],outline=RED,width=2,fill=(255,240,240))
    dc="DATE CHECK: Every story happened or was first reported on Tue 24 Nov 2026; wires read to 23:00 UTC. LEFT OUT (not 24 Nov): Hormuz mine claims (23 Nov) \u00b7 Nvidia Huang return (23 Nov) \u00b7 EU sanctions package (23 Nov) \u00b7 COP31 no deal (22 Nov) \u00b7 El Chapo arrest (Fri 20 Nov). NOT YET: Shenzhou-24 launch (25 Nov) \u00b7 Huawei sentencing (Sep 2027)."
    yy=936
    for ln in wrap(dc,F(SANS,11),988,d)[:2]:
        txt(d,18,yy,ln,F(SANS,11)); yy+=14
    txt(d,12,974,"Sources: Saudi officials \u00b7 CCDI \u00b7 US court \u00b7 Ukrainian officials \u00b7 CAS \u00b7 UKMTO \u00b7 Reuters \u00b7 AP. CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on record \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side.",F(SANS,9),SLATE)
    txt(d,12,990,"Scenes are drawn in code, not photographs. Tuesday 24 November 2026 \u00b7 38 stories \u00b7 6 regions \u00b7 13 fields.",F(SANS,9),SLATE)
    out=os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR","out"),"entry.png"); os.makedirs(os.path.dirname(out),exist_ok=True); im.save(out,optimize=True)
if __name__=="__main__": main()
