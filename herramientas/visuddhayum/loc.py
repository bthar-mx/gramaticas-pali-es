import sys,re;sys.path.insert(0,'.')
from lines import lines
D=str.maketrans('၀၁၂၃၄၅၆၇၈၉','0123456789')
out=[]
for p in range(int(sys.argv[1]),int(sys.argv[2])+1):
    L=lines(p)
    for i,l in enumerate(L):
        t=' '.join(l[4]).translate(D)
        m=re.match(r'\(\s*(\d{2,3})\s*\)',t)
        if m and ('ပဒ' in t): out.append((p,i,'H'+m.group(1)))
        elif re.match(r'\(\s*က\s*\)',t): out.append((p,i,'K'))
        elif re.match(r'\(\s*ခ\s*\)',t): out.append((p,i,'C'))
for o in out: print(*o)
