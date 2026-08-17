from PIL import Image, ImageDraw
from pathlib import Path
import math, random

ROOT=Path('nightfall_reboot/src/main/resources/assets/eternal_skies_nightfall/textures')
ENT=ROOT/'entity'; ITEM=ROOT/'item'
ENT.mkdir(parents=True,exist_ok=True); ITEM.mkdir(parents=True,exist_ok=True)

def rect(draw, box, color):
    x0,y0,x1,y1=box
    draw.rectangle([int(math.floor(x0)),int(math.floor(y0)),int(math.ceil(x1))-1,int(math.ceil(y1))-1], fill=color)

def faces(u,v,dx,dy,dz):
    return {
      'top':(u+dz,v,u+dz+dx,v+dz),
      'bottom':(u+dz+dx,v,u+dz+2*dx,v+dz),
      'left':(u,v+dz,u+dz,v+dz+dy),
      'front':(u+dz,v+dz,u+dz+dx,v+dz+dy),
      'right':(u+dz+dx,v+dz,u+2*dz+dx,v+dz+dy),
      'back':(u+2*dz+dx,v+dz,u+2*dz+2*dx,v+dz+dy),
    }

def fill_cube(img,u,v,dx,dy,dz,base,top=None,side=None,shadow=None):
    d=ImageDraw.Draw(img); f=faces(u,v,dx,dy,dz)
    rect(d,f['top'],top or base); rect(d,f['bottom'],shadow or base); rect(d,f['front'],base)
    rect(d,f['back'],shadow or base); rect(d,f['left'],side or shadow or base); rect(d,f['right'],side or shadow or base)
    return f

def pixel_noise(img, box, colors, amount=0.12, seed=0, transparent_skip=True):
    rng=random.Random(seed); x0,y0,x1,y1=[int(round(z)) for z in box]
    for y in range(y0,max(y0,y1)):
      for x in range(x0,max(x0,x1)):
        if rng.random()<amount:
          if transparent_skip and img.getpixel((x,y))[3]==0: continue
          img.putpixel((x,y),rng.choice(colors))

D=Image.new('RGBA',(128,128),(0,0,0,0)); G=Image.new('RGBA',(128,128),(0,0,0,0)); d=ImageDraw.Draw(D); g=ImageDraw.Draw(G)
skin=(190,181,218,255); skin_hi=(225,219,239,255); skin_sh=(120,108,157,255)
hair=(225,222,242,255); hair_hi=(247,245,255,255); hair_sh=(157,148,190,255)
ivory=(205,202,218,255); ivory_hi=(237,234,244,255); ivory_sh=(145,137,170,255)
lav=(151,132,199,255); lavender_hi=(191,170,232,255); dusk=(59,44,90,255); dusk2=(86,58,124,255)
gold=(183,145,78,255); gold_hi=(230,196,120,255); gold_sh=(120,88,53,255)
crystal=(151,84,226,255); glow=(205,129,255,255); eye=(190,105,255,255)
f=fill_cube(D,0,0,7,8,7,skin,skin_hi,skin_sh,skin_sh); x0,y0,x1,y1=[int(round(z)) for z in f['front']]
for y in range(y0,y1):
    if y-y0>=5: D.putpixel((x0,y),skin_sh); D.putpixel((x1-1,y),skin_sh)
for x in (x0+1,x0+4):
    D.putpixel((x,y0+3),eye); D.putpixel((x+1,y0+3),eye); G.putpixel((x,y0+3),eye); G.putpixel((x+1,y0+3),glow)
D.putpixel((x0+3,y0+4),skin_sh); D.putpixel((x0+3,y0+5),skin_sh)
for x in range(x0+2,x0+5): D.putpixel((x,y0+6),(104,83,126,255))
D.putpixel((x0+3,y0+1),lavender_hi); D.putpixel((x0+2,y0+2),lav); D.putpixel((x0+4,y0+2),lav); G.putpixel((x0+3,y0+1),(176,118,244,190))
hf=fill_cube(D,32,0,7,8,7,hair,hair_hi,hair_sh,hair_sh); fx0,fy0,fx1,fy1=[int(round(z)) for z in hf['front']]
rect(d,(fx0,fy0,fx1,fy0+2),hair_hi); rect(d,(fx0,fy0+2,fx1,fy1),(0,0,0,0))
for yy in range(fy0+2,min(fy1,fy0+5)):
    D.putpixel((fx0,yy),hair_sh)
    if fx1-1<128:D.putpixel((fx1-1,yy),hair)
for px,ln in [(fx0+1,3),(fx0+2,2),(fx0+4,3),(fx0+5,2)]:
    for yy in range(fy0, min(fy1,fy0+ln)): D.putpixel((px,yy),hair_hi if yy==fy0 else hair)
pixel_noise(D,hf['top'],[hair_hi,hair_sh],0.18,1); pixel_noise(D,hf['back'],[hair_hi,hair_sh],0.15,2)
fill_cube(D,64,0,4,2,2,skin,skin_hi,skin_sh,skin_sh); fill_cube(D,64,4,4,2,2,skin,skin_hi,skin_sh,skin_sh)
for u in (76,84,92):
    dx=2 if u!=92 else 5; fill_cube(D,u,0,dx,7,2,hair,hair_hi,hair_sh,hair_sh); pixel_noise(D,(u,0,min(128,u+16),16),[hair_hi,hair_sh],0.10,u)
bf=fill_cube(D,0,20,7,11,4,dusk2,(104,77,144,255),dusk,dusk); fx0,fy0,fx1,fy1=[int(round(z)) for z in bf['front']]
for y in range(fy0+1,fy1-1):
    D.putpixel((fx0+3,y),lav)
    if y%3!=0: D.putpixel((fx0+2,y),gold)
for p in [(fx0+3,fy0+3),(fx0+2,fy0+4),(fx0+4,fy0+4),(fx0+3,fy0+5)]: D.putpixel(p,gold_hi)
fill_cube(D,26,20,8.2,3,5.2,ivory,ivory_hi,ivory_sh,ivory_sh); pixel_noise(D,(26,20,55,34),[ivory_hi,lav,gold],0.06,10)
cg=fill_cube(D,54,20,3,3,1,crystal,glow,dusk2,dusk2)
for r in faces(54,20,3,3,1).values():
    a,b,c,e=[int(round(z)) for z in r]
    if c>a and e>b: G.putpixel((min(127,(a+c)//2),min(127,(b+e)//2)),glow)
robe_specs=[(0,40,5.4,11,1),(16,40,6,12,1),(32,40,1,10,4),(42,40,1,10,4)]
for idx,(u,v,dx,dy,dz) in enumerate(robe_specs):
    rf=fill_cube(D,u,v,dx,dy,dz,ivory,ivory_hi,lav,ivory_sh)
    for face_name in ('front','back'):
      a,b,c,e=[int(round(z)) for z in rf[face_name]]
      if c<=a or e<=b: continue
      for y in range(b,e):
        if y-b>=max(2,(e-b)-4):
          for x in range(a,c):
            if (x+y+idx)%3: D.putpixel((x,y),lav if (x+y)%2 else dusk2)
        elif (y-b)%4==1 and c-a>2: D.putpixel((a+1,y),gold)
      for x,y in [(a+1,e-2),(c-2,e-3)]:
        if 0<=x<128 and 0<=y<128: D.putpixel((x,y),(0,0,0,0))
for spec,col in [((0,56,3,12,3),ivory),((14,56,3,12,3),ivory)]:
    fill_cube(D,*spec,col,ivory_hi,ivory_sh,lav); pixel_noise(D,(spec[0],spec[1],spec[0]+16,spec[1]+18),[lavender_hi,ivory_hi],0.07,spec[0]+20)
for spec in [(28,56,4.5,4,4.6),(48,56,4.5,4,4.6)]:
    fill_cube(D,*spec,ivory,ivory_hi,gold_sh,lav); pixel_noise(D,(spec[0],spec[1],min(128,spec[0]+22),min(128,spec[1]+12)),[gold,gold_hi,lav],0.10,spec[0])
for spec in [(68,56,3.3,4,3.4),(84,56,3.3,4,3.4)]: fill_cube(D,*spec,gold,gold_hi,gold_sh,dusk2)
for spec in [(0,76,3.2,12,3),(14,76,3.2,12,3)]: fill_cube(D,*spec,(108,91,148,255),lav,dusk,dusk)
for spec in [(28,76,3.7,6.8,3.5),(46,76,3.7,6.8,3.5)]:
    fill_cube(D,*spec,ivory,ivory_hi,gold_sh,lav); pixel_noise(D,(spec[0],spec[1],spec[0]+18,spec[1]+15),[gold,gold_hi,lav],0.10,spec[0]+5)
wing_specs=[(0,96,5,11,1.1,0),(16,96,8,13,1,1),(38,96,8,11,0.9,2),(60,96,2,10,0.7,3),(66,96,2,8,0.7,4),(0,110,5,11,1.1,5),(16,110,8,13,1,6),(38,110,8,11,0.9,7),(60,110,2,10,0.7,8),(66,110,2,8,0.7,9)]
for u,v,dx,dy,dz,idx in wing_specs:
    wf=fill_cube(D,u,v,dx,dy,dz,ivory,ivory_hi,lav,lav)
    for name in ('front','back'):
      a,b,c,e=[int(round(z)) for z in wf[name]]; h=max(1,e-b)
      for y in range(b,e):
        t=(y-b)/h; col=ivory if t<0.45 else (lavender_hi if t<0.72 else lav)
        if t>0.86: col=dusk2
        for x in range(a,c):
          if 0<=x<128 and 0<=y<128: D.putpixel((x,y),col)
      for y in range(b,min(e,b+3)):
        if a<c: D.putpixel((a,y),gold_hi)
      if c-a>=4 and e-b>=6:
        for k in range(2):
          xx=a+1+((idx+k*2)%(max(1,c-a-2))); yy=b+3+k*2
          if yy<e: D.putpixel((xx,yy),crystal); G.putpixel((xx,yy),(181,104,255,180))
        for x,y in [(a+1,e-2),(c-2,e-4)]:
          if 0<=x<128 and 0<=y<128: D.putpixel((x,y),(0,0,0,0))
for spec in [(78,96,6,0.8,0.8),(78,99,6,0.8,0.8),(96,96,0.8,0.8,6),(100,96,0.8,0.8,6),(110,96,1.2,2.2,0.8),(116,96,1,1.8,0.7)]:
    hf=fill_cube(D,*spec,gold_hi,(246,220,151,255),gold,gold_sh)
    for r in hf.values(): rect(g,r,(244,194,255,225))
pixel_noise(D,(0,20,64,95),[lavender_hi,gold_hi],0.025,999); D.save(ENT/'duskborn.png'); G.save(ENT/'duskborn_glow.png')

S=Image.new('RGBA',(128,128),(0,0,0,0)); SG=Image.new('RGBA',(128,128),(0,0,0,0))
cloud=(91,86,128,255); cloud_hi=(133,126,170,255); cloud_mid=(108,100,148,255); cloud_sh=(55,50,86,255); cloud_deep=(41,36,70,255); face=(27,20,48,255); face_hi=(43,31,72,255)
lightning=(201,113,255,255); lightning_hi=(239,189,255,255); core=(154,76,231,255); core2=(113,56,183,255)
storm_specs=[(0,0,11,9,9),(40,0,8,6,7),(70,0,6.4,6,6),(94,0,6.4,6,6),(0,22,7.6,6.4,7),(32,22,7.6,6.4,7),(64,22,8.6,6.4,6),(96,22,8.8,5.6,7.6),(0,52,6,4.4,5.6),(26,52,4,3.2,4),(44,52,2.4,2,2.4)]
for i,spec in enumerate(storm_specs):
    ff=fill_cube(S,*spec,cloud,cloud_hi,cloud_mid,cloud_sh)
    for r in ff.values():
      a,b,c,e=[int(round(z)) for z in r]
      if c<=a or e<=b: continue
      for x in range(a,min(c,a+2)):
        if 0<=x<128 and 0<=b<128: S.putpixel((x,b),cloud_hi)
      for x in range(max(a,c-2),c):
        if 0<=x<128 and 0<=e-1<128:S.putpixel((x,e-1),cloud_sh)
    pixel_noise(S,(spec[0],spec[1],min(128,spec[0]+34),min(128,spec[1]+22)),[cloud_hi,cloud_mid,cloud_sh],0.055,200+i)
fill_cube(S,0,42,7.6,4.8,1,face,face_hi,cloud_deep,cloud_deep)
for spec in [(20,42,2,2,1),(28,42,2,2,1)]:
    ef=fill_cube(S,*spec,lightning,lightning_hi,core2,core2)
    for r in ef.values(): rect(ImageDraw.Draw(SG),r,lightning_hi)
fill_cube(S,38,42,6,6,1.4,cloud_deep,cloud_sh,face,face)
cr=fill_cube(S,64,42,4.4,4.4,1.7,core,lightning_hi,core2,core2)
for r in cr.values(): rect(ImageDraw.Draw(SG),r,lightning)
rr=fill_cube(S,84,42,1.4,3.8,0.6,lightning_hi,lightning_hi,lightning,core)
for r in rr.values(): rect(ImageDraw.Draw(SG),r,lightning_hi)
for spec in [(58,52,2,2,2),(68,52,1.6,1.6,1.6),(78,52,1.4,1.4,1.4)]:
    of=fill_cube(S,*spec,core,lightning_hi,core2,core2)
    for r in of.values(): rect(ImageDraw.Draw(SG),r,(190,106,255,210))
S.save(ENT/'stormling.png'); SG.save(ENT/'stormling_glow.png')

im=Image.new('RGBA',(16,16),(0,0,0,0)); dr=ImageDraw.Draw(im); poly=[(8,1),(11,4),(10,7),(13,9),(9,15),(5,13),(4,8),(6,5)]
dr.polygon(poly,fill=(84,46,133,255)); dr.polygon([(8,2),(10,4),(8,12),(6,12),(5,8),(7,5)],fill=(154,91,213,255)); dr.polygon([(8,2),(9,4),(8,10),(7,9)],fill=(220,172,255,255)); dr.point((10,9),fill=(237,102,255,255)); dr.point((6,6),fill=(237,198,255,255)); im.save(ITEM/'dusk_shard.png')
im=Image.new('RGBA',(16,16),(0,0,0,0)); dr=ImageDraw.Draw(im)
for cx,cy,r,c in [(5,6,3,(75,70,108,255)),(10,6,3,(91,84,126,255)),(6,10,3,(65,59,96,255)),(10,10,3,(80,72,116,255))]: dr.rectangle((cx-r//2,cy-r//2,cx+r//2+1,cy+r//2+1),fill=c)
dr.polygon([(8,3),(12,8),(8,13),(4,8)],fill=(129,66,203,255)); dr.polygon([(8,4),(10,8),(8,11),(6,8)],fill=(221,143,255,255)); dr.point((8,6),fill=(251,213,255,255)); dr.point((11,4),fill=(196,117,255,255)); dr.point((3,9),fill=(196,117,255,255)); im.save(ITEM/'storm_core.png')
print('painted Nightfall art assets')