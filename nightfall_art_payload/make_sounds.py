import numpy as np
import soundfile as sf
from pathlib import Path
SR=44100
OUT=Path('nightfall_reboot/src/main/resources/assets/eternal_skies_nightfall/sounds')
(OUT/'mob/duskborn').mkdir(parents=True, exist_ok=True)
(OUT/'mob/stormling').mkdir(parents=True, exist_ok=True)
rng=np.random.default_rng(303)

def env(n, attack=.02, release=.25):
    a=max(1,int(n*attack)); r=max(1,int(n*release)); e=np.ones(n)
    e[:a]=np.linspace(0,1,a); e[-r:]=np.linspace(1,0,r)
    return e

def smooth_noise(n, width=120):
    x=rng.normal(0,1,n); k=np.ones(width)/width; y=np.convolve(x,k,mode='same'); m=np.max(np.abs(y)) or 1
    return y/m

def high_noise(n, width=4):
    x=rng.normal(0,1,n); y=x-np.convolve(x,np.ones(width)/width,mode='same')
    return y/(np.max(np.abs(y)) or 1)

def sine_sweep(t,f0,f1,phase=0):
    k=np.log(max(f1,1)/max(f0,1))/max(t[-1],1e-6)
    phase_arr=2*np.pi*f0*(np.exp(k*t)-1)/k if abs(k)>1e-8 else 2*np.pi*f0*t
    return np.sin(phase_arr+phase)

def save(name, data):
    data=np.asarray(data,float); data=np.nan_to_num(data); peak=np.max(np.abs(data)) or 1
    data=np.clip(data/(peak*1.08),-1,1); oggp=OUT/(name+'.ogg')
    sf.write(str(oggp), data.astype(np.float32), SR, format='OGG', subtype='VORBIS')
    print(oggp.relative_to(OUT))

for idx,(fund,dur) in enumerate([(196,2.2),(220,2.0)],1):
    n=int(SR*dur); t=np.arange(n)/SR
    wind=smooth_noise(n,2600)*0.32 + smooth_noise(n,420)*0.08
    shimmer=np.sin(2*np.pi*fund*t)*0.10 + np.sin(2*np.pi*fund*1.5*t+0.7)*0.06 + np.sin(2*np.pi*fund*2.03*t+1.2)*0.035
    wob=0.6+0.4*np.sin(2*np.pi*0.34*t+idx); bell=np.sin(2*np.pi*(880+idx*55)*t)*np.exp(-3.0*t)*0.10
    save(f'mob/duskborn/ambient{idx}', (wind*wob+shimmer*wob+bell)*env(n,.10,.35))
for idx,offset in enumerate([0.0,0.17],1):
    dur=.88; n=int(SR*dur); t=np.arange(n)/SR; rise=np.linspace(0,1,n)**1.6
    hiss=high_noise(n,10)*rise*0.24; chirp=sine_sweep(t,360+offset*100,1600+offset*220)*rise*0.18
    bell=np.sin(2*np.pi*1240*t)*np.exp(-((t-.68)/.12)**2)*0.25
    save(f'mob/duskborn/veil{idx}',(hiss+chirp+bell)*env(n,.02,.18))
for idx in (1,2):
    dur=.46; n=int(SR*dur); t=np.arange(n)/SR
    whoosh=smooth_noise(n,80)*np.sin(np.pi*np.clip(t/dur,0,1))**1.4; low=np.sin(2*np.pi*(95+idx*8)*t)*np.exp(-5*t)
    save(f'mob/duskborn/flap{idx}',whoosh*.55+low*.16)
for idx,f0 in enumerate([430,470],1):
    dur=.48;n=int(SR*dur);t=np.arange(n)/SR
    chirp=sine_sweep(t,f0,1850)*np.exp(-2.7*t)*.32; sparkle=np.sin(2*np.pi*2200*t)*np.exp(-8*t)*.16; snap=high_noise(n,3)*np.exp(-18*t)*.20
    save(f'mob/duskborn/bolt{idx}',(chirp+sparkle+snap)*env(n,.01,.28))
for idx,f in enumerate([250,285],1):
    dur=.42;n=int(SR*dur);t=np.arange(n)/SR; tone=sine_sweep(t,f,f*.63)*.35; breath=high_noise(n,18)*.18
    save(f'mob/duskborn/hurt{idx}',(tone+breath)*env(n,.01,.48))
dur=1.65;n=int(SR*dur);t=np.arange(n)/SR
fall=sine_sweep(t,310,92)*.34 + sine_sweep(t,620,150,1.2)*.16; ash=smooth_noise(n,900)*.22*(1-np.linspace(0,1,n)*.3); chime=np.sin(2*np.pi*980*t)*np.exp(-3.5*t)*.13
save('mob/duskborn/death',(fall+ash+chime)*env(n,.02,.35))
for idx,base in enumerate([62,71],1):
    dur=1.9;n=int(SR*dur);t=np.arange(n)/SR
    rum=np.sin(2*np.pi*base*t)*.20 + np.sin(2*np.pi*base*.51*t+.5)*.13; cloud=smooth_noise(n,1800)*.30; crack=np.zeros(n)
    for _ in range(10):
        p=rng.integers(0,n-500); ln=rng.integers(80,420); crack[p:p+ln]+=high_noise(ln,2)*np.linspace(1,0,ln)*rng.uniform(.05,.15)
    save(f'mob/stormling/ambient{idx}',(rum+cloud+crack)*env(n,.08,.30))
dur=1.82;n=int(SR*dur);t=np.arange(n)/SR; rise=np.linspace(0,1,n)
charge=sine_sweep(t,120,760)*(.10+.25*rise); charge+=sine_sweep(t,240,1450,1.0)*(.05+.16*rise); charge+=high_noise(n,3)*(.02+.19*rise**2); charge+=smooth_noise(n,100)*(.08+.07*rise)
save('mob/stormling/charge',charge*env(n,.01,.07))
for idx,f in enumerate([720,860],1):
    dur=.24;n=int(SR*dur);t=np.arange(n)/SR; click=np.sin(2*np.pi*f*t)*np.exp(-16*t)*.38 + high_noise(n,2)*np.exp(-28*t)*.16
    save(f'mob/stormling/pulse{idx}',click*env(n,.005,.35))
for idx,f in enumerate([155,185],1):
    dur=.36;n=int(SR*dur);t=np.arange(n)/SR; crack=high_noise(n,2)*np.exp(-8*t)*.35 + sine_sweep(t,f,f*.7)*.24
    save(f'mob/stormling/hurt{idx}',crack*env(n,.005,.35))
dur=1.2;n=int(SR*dur);t=np.arange(n)/SR
thump=np.sin(2*np.pi*58*t)*np.exp(-4.7*t)*.55 + np.sin(2*np.pi*91*t)*np.exp(-7*t)*.28; burst=smooth_noise(n,55)*np.exp(-3.2*t)*.45; spark=high_noise(n,2)*np.exp(-9*t)*.24; ring=sine_sweep(t,540,170)*np.exp(-3.3*t)*.16
save('mob/stormling/discharge',(thump+burst+spark+ring)*env(n,.002,.25))
dur=.75;n=int(SR*dur);t=np.arange(n)/SR
collapse=sine_sweep(t,210,70)*.34 + smooth_noise(n,130)*np.exp(-4*t)*.30 + high_noise(n,2)*np.exp(-13*t)*.12
save('mob/stormling/death',collapse*env(n,.005,.35))