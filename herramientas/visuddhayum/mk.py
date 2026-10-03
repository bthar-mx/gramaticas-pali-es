import sys,re,os;sys.path.insert(0,'.')
from lines import lines,img,B
from PIL import Image
D=str.maketrans('၀၁၂၃၄၅၆၇၈၉','0123456789')
OUT=B+'/_crops/nama'; os.makedirs(OUT,exist_ok=True)
a,b=int(sys.argv[1]),int(sys.argv[2])
# sequence of markers
seq=[]
for p in range(a,b+1):
    L=lines(p)
    for i,l in enumerate(L):
        t=' '.join(l[4]).translate(D)
        m=re.match(r'\(\s*(\d{2,3})\s*\)',t)
        if m and 'ပဒ' in t: seq.append(['H',p,i,int(m.group(1))])
        elif re.match(r'\(\s*ခ\s*\)',t): seq.append(['C',p,i,None])
def seg(p,i0,i1):
    L=lines(p);im=Image.open(B+'/img/'+img(p))
    i1=min(i1,len(L)-1); y0=max(0,L[i0][1]-14); y1=min(im.size[1],L[i1][3]+14)
    return im.crop((0,y0,im.size[0],y1))
def span(p,i,n):
    """n lines from (p,i), continuing onto next page if needed"""
    L=lines(p); parts=[]
    j=min(len(L)-1,i+n-1); parts.append(seg(p,i,j)); rest=n-(j-i+1)
    if rest>0 and p+1<=b+1:
        L2=lines(p+1); parts.append(seg(p+1,1,min(len(L2)-1,rest)))  # skip running head
    return parts
hs=[k for k,s in enumerate(seq) if s[0]=='H']
for k in hs:
    s=seq[k]; n=s[3]; parts=span(s[1],s[2],5)
    nxt=seq[k+1] if k+1<len(seq) else None
    if nxt and nxt[0]=='C': parts+=span(nxt[1],nxt[2],7)
    W=max(x.size[0] for x in parts); H=sum(x.size[1] for x in parts)+8*(len(parts)-1)
    S=Image.new('RGB',(W,H),(255,255,255));y=0
    for x in parts: S.paste(x,(0,y)); y+=x.size[1]+8
    if H>1500: S=S.resize((int(W*1500/H),1500))
    S.save(f'{OUT}/h{n:03d}-p{s[1]}.jpg',quality=80)
    print(n, s[1], 'C' if nxt and nxt[0]=='C' else '-', S.size)
