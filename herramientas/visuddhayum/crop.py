import sys,os
sys.path.insert(0,os.path.expanduser('~/vh'))
from lines import lines,img,B
from PIL import Image
# usage: crop.py page a b out  (line indices inclusive) ; or page y0 y1 out with y prefix
p=int(sys.argv[1]); a=sys.argv[2]; b=sys.argv[3]; out=sys.argv[4]
im=Image.open(B+'/img/'+img(p))
if a.startswith('y'): y0,y1=int(a[1:]),int(b[1:])
else:
    L=lines(p); y0=L[int(a)][1]-12; y1=L[int(b)][3]+12
im.crop((0,max(0,y0),im.size[0],min(im.size[1],y1))).save(out,quality=85)
print(out,y0,y1)
