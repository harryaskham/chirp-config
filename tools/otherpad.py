"""otherpad.py ID P TAG GAIN [PATCH] [TH] : spans where the record's other stem sits within TH dB (default -30) of the mix (5 s windows,
merged), padtrans'd from the other stem (0.5 s, 3 voices, 80-2k) and appended LAST (RNG-safe) as track 'oth' -> $OTHERPAD_DIR (default /tmp/lt/otherpad)/P-TAG.json and P-TAG-notes.json.
chirper-one, obZen: Dancers v10 +0.21..+0.27, Pravus v11 +0.42..+0.53 (pad 0/+4 dB)."""
import sys,os,json,subprocess,copy
import numpy as np
ID,P,TAG,G=sys.argv[1:5];PATCH=sys.argv[5] if len(sys.argv)>5 else 'pad';TH=float(sys.argv[6]) if len(sys.argv)>6 else -30
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));C=os.environ.get('OTHERPAD_DIR','/tmp/lt/otherpad');os.makedirs(C,exist_ok=True)
sys.path.insert(0,f'{R}/tools');import likeness as L
SR=48000;y=L.load(f'{R}/ref/stems/htdemucs_6s/{ID}/other.wav').mean(1);m=L.load(f'{R}/ref/{ID}.wav').mean(1)
w=5;spans=[]
for t in range(0,len(m)//SR-w+1,w):
    d=10*np.log10((y[t*SR:(t+w)*SR]**2).mean()+1e-12)-10*np.log10((m[t*SR:(t+w)*SR]**2).mean()+1e-12)
    if d>TH:
        if spans and spans[-1][1]==t:spans[-1][1]=t+w
        else:spans.append([t,t+w])
notes=[]
for a,b in spans:
    o=subprocess.run(['python3','tools/padtrans.py',f'ref/stems/htdemucs_6s/{ID}/other.wav','--from',str(a),'--to',str(b),'--win','0.5','--floor','-50','--voices','3','--range','80-2000','--json'],cwd=R,capture_output=True,text=True).stdout
    try:notes+=json.loads(o)
    except Exception:pass
subprocess.run(['python3','tools/songfmt.py','json',f'songs/{ID}.yaml','-o',f'{C}/{P}-opcur.json'],cwd=R,capture_output=True)
d=json.load(open(f'{C}/{P}-opcur.json'))
d['tracks'].append({'name':'oth','patch':PATCH,'gain':G,'notes':notes})
json.dump(d,open(f'{C}/{P}-{TAG}.json','w'),indent=1)
json.dump(notes,open(f'{C}/{P}-{TAG}-notes.json','w'))
print(ID,TAG,'spans',spans,'notes',len(notes))
