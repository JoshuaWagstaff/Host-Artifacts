from PIL import Image, ImageDraw
from pathlib import Path
import random

random.seed(81726)
ROOT=Path('nightfall_reboot/src/main/resources/assets/eternal_skies_nightfall/textures/entity')
CLEAR=(0,0,0,0)

def clamp(v): return max(0,min(255,int(v)))
def mix(a,b,t): return tuple(clamp(a[i]*(1-t)+b[i]*t) for i in range(3))+(255,)
def put(im,x,y,c):
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),c)

def shade_rect(im,x,y,w,h,base,hi,sh,outline=.28,grain=.08):
    x,y,w,h=map(int,(round(x),round(y),round(w),round(h)))
    if w<1 or h<1:return
    pix=im.load()
    for yy in range(y,y+h):
        for xx in range(x,x+w):
            if not (0<=xx<im.width and 0<=yy<im.height): continue
            tx=(xx-x)/max(1,w-1); ty=(yy-y)/max(1,h-1)
            edge=min(xx-x,x+w-1-xx,yy-y,y+h-1-yy)
            light=(1-tx)*.12+(1-ty)*.12
            dark=tx*.07+ty*.11
            c=mix(base,hi,light)
            c=mix(c,sh,dark)
            if edge==0: c=mix(c,sh,outline)
            if random.random()<grain:
                c=mix(c, random.choice([hi,sh]), random.uniform(.08,.20))
            pix[xx,yy]=c

def cube_uv(im,u,v,dx,dy,dz,base,hi,sh,grain=.05):
    dx=max(1,int(round(dx)));dy=max(1,int(round(dy)));dz=max(1,int(round(dz)))
    shade_rect(im,u+dz,v,dx,dz,hi,hi,base,.18,grain*.6)
    shade_rect(im,u+dz+dx,v,dx,dz,sh,base,sh,.25,grain*.6)
    shade_rect(im,u,v+dz,dz,dy,base,hi,sh,.30,grain)
    shade_rect(im,u+dz,v+dz,dx,dy,base,hi,sh,.30,grain)
    shade_rect(im,u+dz+dx,v+dz,dz,dy,base,hi,sh,.34,grain)
    shade_rect(im,u+dz+dx+dz,v+dz,dx,dy,base,hi,sh,.34,grain)

def front_rect(u,v,dx,dy,dz):
    return int(round(u+dz)),int(round(v+dz)),int(round(dx)),int(round(dy))

SKIN=(194,190,218,255); SKIN_HI=(232,229,244,255); SKIN_SH=(145,136,178,255)
HAIR=(230,229,244,255); HAIR_HI=(251,250,255,255); HAIR_SH=(170,165,202,255); HAIR_DEEP=(118,109,158,255)
LAV=(177,170,215,255); LAV_HI=(221,217,239,255); LAV_SH=(116,103,162,255); LAV_DEEP=(67,55,111,255)
IV=(229,225,211,255); IV_HI=(253,250,237,255); IV_SH=(178,170,157,255)
GOLD=(194,151,61,255); GOLD_HI=(244,207,100,255); GOLD_SH=(117,82,30,255)
VIO=(135,61,216,255); VIO_HI=(213,137,255,255); VIO_DEEP=(71,26,124,255)
INK=(49,38,75,255); SOFT_INK=(78,64,108,255)

im=Image.new('RGBA',(256,256),CLEAR); glow=Image.new('RGBA',(256,256),CLEAR)

# Head: 2x texel density compared with the old prototype so eyes, mouth, markings and hair read as intentional pixels.
cube_uv(im,0,0,14,16,14,SKIN,SKIN_HI,SKIN_SH,.05)
fx,fy,fw,fh=front_rect(0,0,14,16,14)
for yy in range(fy,fy+fh):
    local=yy-fy
    for xx in range(fx,fx+fw):
        lx=xx-fx
        if lx in (0,13): put(im,xx,yy,mix(SKIN,SKIN_SH,.35))
        if local>=12 and lx in (1,12): put(im,xx,yy,mix(SKIN,SKIN_SH,.22))
for p in [(3,5),(4,4),(5,4),(8,4),(9,4),(10,5)]: put(im,fx+p[0],fy+p[1],SOFT_INK)
for cx in (4,9):
    put(im,fx+cx-1,fy+6,INK); put(im,fx+cx,fy+6,VIO_HI); put(im,fx+cx+1,fy+6,INK)
    put(im,fx+cx-1,fy+7,SKIN_SH); put(im,fx+cx,fy+7,SKIN_HI); put(im,fx+cx+1,fy+7,SKIN_SH)
    put(glow,fx+cx,fy+6,(235,180,255,255))
for p,c in [((6,7),SKIN_HI),((6,8),SKIN_HI),((7,8),SKIN_SH),((6,9),SKIN_SH),((7,10),SKIN_HI),
            ((5,12),SKIN_SH),((6,12),INK),((7,12),INK),((8,12),SKIN_SH),((6,13),SKIN_HI),((7,13),SKIN_HI)]:
    put(im,fx+p[0],fy+p[1],c)
for p,c in [((6,1),GOLD_HI),((7,1),GOLD_HI),((5,2),GOLD),((8,2),GOLD),((6,3),VIO_HI),((7,3),VIO_HI)]:
    put(im,fx+p[0],fy+p[1],c)
put(glow,fx+6,fy+3,(211,136,255,180)); put(glow,fx+7,fy+3,(211,136,255,180))

# Ears and layered swept hair.
for u in (164,190): cube_uv(im,u,0,8,4,4,SKIN,SKIN_HI,SKIN_SH,.03)
for args in [(60,0,15,4,15),(120,0,6,5,1),(142,0,6,5,1),(0,32,4,15,4),(20,32,4,15,4),(40,32,10,17,3)]:
    cube_uv(im,*args,HAIR,HAIR_HI,HAIR_SH,.08)
for u,v,dx,dy,dz in [(120,0,6,5,1),(142,0,6,5,1)]:
    x,y,w,h=front_rect(u,v,dx,dy,dz)
    for yy in range(y,y+h):
        for off in (1,4):
            if (yy-y+off)%3==0: put(im,x+off,yy,HAIR_DEEP)
for u in (0,20):
    x,y,w,h=front_rect(u,32,4,15,4)
    for yy in range(y,y+h):
        if (yy-y)%4==1: put(im,x,yy,HAIR_HI)
        if (yy-y)%5==3: put(im,x+w-1,yy,HAIR_DEEP)

# Fragmented gold halo.
for args in [(74,32,12,1,1),(104,32,12,1,1),(134,32,1,1,12),(150,32,1,1,12),(166,32,2,4,1),(176,32,2,4,1)]:
    cube_uv(im,*args,GOLD,GOLD_HI,GOLD_SH,.02)
for y in range(32,56):
    for x in range(70,190):
        r,g,b,a=im.getpixel((x,y))
        if a and r>130 and g>80 and r>g:
            glow.putpixel((x,y),(255,219,111,210))

# Layered Aether-native armor/robes.
cube_uv(im,0,64,14,24,8,LAV,LAV_HI,LAV_SH,.07)
fx,fy,fw,fh=front_rect(0,64,14,24,8)
for yy in range(fy+1,fy+fh-1):
    for xx in range(fx+5,fx+9): put(im,xx,yy,IV_HI if xx in (fx+6,fx+7) else IV)
    if yy%6==0:
        put(im,fx+2,yy,GOLD); put(im,fx+11,yy,GOLD)
for yy in range(fy+3,fy+fh-2,5):
    put(im,fx+3,yy,GOLD_HI); put(im,fx+10,yy,GOLD_HI)
for p in [(2,4),(11,7),(3,12),(10,15),(2,20),(11,21)]: put(im,fx+p[0],fy+p[1],IV_HI)
cube_uv(im,48,64,16,6,10,IV,IV_HI,IV_SH,.05)
cube_uv(im,104,64,10,12,2,IV,IV_HI,IV_SH,.05)
x,y,w,h=front_rect(104,64,10,12,2)
for yy in range(y+1,y+h-1):
    put(im,x+1,yy,GOLD_SH); put(im,x+w-2,yy,GOLD)
for p in [(4,2),(5,2),(3,6),(6,6),(4,9),(5,9)]: put(im,x+p[0],y+p[1],GOLD_HI)
cube_uv(im,132,64,6,6,2,VIO,VIO_HI,VIO_DEEP,.02)
for yy in range(64,80):
    for xx in range(130,150):
        r,g,b,a=im.getpixel((xx,yy))
        if a and b>130 and r>90: glow.putpixel((xx,yy),(220,145,255,235))
cube_uv(im,152,64,15,3,9,GOLD,GOLD_HI,GOLD_SH,.04)

for args in [(0,98,11,21,2),(28,98,12,23,2),(60,98,2,19,8),(82,98,2,19,8)]:
    cube_uv(im,*args,LAV,LAV_HI,LAV_DEEP,.07)
for u,v,dx,dy,dz in [(0,98,11,21,2),(28,98,12,23,2)]:
    x,y,w,h=front_rect(u,v,dx,dy,dz)
    for xx in range(x,x+w):
        put(im,xx,y+h-2,GOLD if xx%2==0 else VIO)
        put(im,xx,y+h-1,LAV_DEEP)
    for p in [(2,5),(w-3,7),(3,12),(w-4,15)]:
        if 0<=p[0]<w and 0<=p[1]<h: put(im,x+p[0],y+p[1],GOLD_HI)

# Arms, pauldrons, bracers, hands, legs and greaves.
for args in [(0,128,6,24,6),(28,128,6,24,6)]: cube_uv(im,*args,LAV,LAV_HI,LAV_SH,.06)
for args in [(56,128,9,8,9),(96,128,9,8,9)]: cube_uv(im,*args,IV,IV_HI,IV_SH,.06)
for args in [(136,128,7,8,7),(166,128,7,8,7)]: cube_uv(im,*args,GOLD,GOLD_HI,GOLD_SH,.05)
for u in (0,28):
    x,y,w,h=front_rect(u,128,6,24,6)
    for yy in range(y+h-5,y+h):
        for xx in range(x,x+w): put(im,xx,yy,SKIN if yy<y+h-2 else SKIN_SH)
for args in [(0,162,6,24,6),(28,162,6,24,6)]: cube_uv(im,*args,LAV_DEEP,LAV,LAV_DEEP,.05)
for args in [(56,162,7,14,7),(88,162,7,14,7)]: cube_uv(im,*args,IV,IV_HI,IV_SH,.07)
for u in (56,88):
    x,y,w,h=front_rect(u,162,7,14,7)
    for yy in range(y+2,y+h-2,4):
        put(im,x+1,yy,GOLD); put(im,x+w-2,yy,GOLD_HI)

# Wings: layered coverts plus separated feather primaries. Pale Aether values dominate; dusk corruption stays at the broken tips.
for v in (198,220):
    cube_uv(im,0,v,17,10,2,IV,IV_HI,IV_SH,.06)
    cube_uv(im,44,v,20,7,2,IV,IV_HI,LAV_SH,.06)
    x,y,w,h=front_rect(0,v,17,10,2)
    for yy in range(y+2,y+h):
        if yy%3==0:
            for xx in range(x+1,x+w-1,4):
                put(im,xx,yy,LAV_SH); put(im,xx+1,yy,IV_HI)
    x2,y2,w2,h2=front_rect(44,v,20,7,2)
    for xx in range(x2+2,x2+w2-2,3): put(im,xx,y2+h2-2,GOLD)
    for u,dx,dy,dz in [(98,4,24,2),(110,4,21,2),(122,3,17,2),(134,3,7,1)]:
        cube_uv(im,u,v,dx,dy,dz,IV,IV_HI,LAV_SH,.04)
        fx,fy,fw,fh=front_rect(u,v,dx,dy,dz)
        for yy in range(fy,fy+fh):
            t=(yy-fy)/max(1,fh-1)
            put(im,fx,yy,GOLD_HI if yy%4 else GOLD)
            if t>.64:
                col=mix(LAV_SH,VIO_DEEP,min(1,(t-.64)/.36))
                for xx in range(fx,fx+fw): put(im,xx,yy,col)
                if t>.78:
                    for xx in range(fx,fx+fw): glow.putpixel((xx,yy),(154,75,234,120 if t<.9 else 190))
        if fh>8:
            yy=fy+int(fh*.76)
            for i in range(min(fw,4)):
                put(im,fx+i,yy+(i%2),VIO_HI)
                glow.putpixel((fx+i,yy+(i%2)),(226,155,255,220))

for x,y in [(9,78),(18,81),(12,88),(21,93),(113,78),(117,84),(159,77),(173,74),(61,143),(101,145),(143,140),(174,140)]:
    put(im,x,y,GOLD_HI)

ROOT.mkdir(parents=True, exist_ok=True)
im.save(ROOT/'duskborn.png')
glow.save(ROOT/'duskborn_glow.png')
print('painted refined Duskborn texture + glow')
