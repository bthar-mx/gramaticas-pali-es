import sys,subprocess,os,csv,io
B=os.path.expanduser('~/mnt/nissaya/ocr/visuddhayum-kaccayana-tika')
def img(p):
    return [f for f in os.listdir(B+'/img') if f.startswith(f'p-{p:03d}-')][0]
def lines(p):
    c=os.path.expanduser(f'~/vh/tsv/{p}.tsv')
    if not os.path.exists(c):
        out=subprocess.run(['tesseract',B+'/img/'+img(p),'stdout','--tessdata-dir',B+'/tessdata','-l','mya','--psm','6','-c','tessedit_create_tsv=1'],capture_output=True,text=True).stdout
        open(c,'w').write(out)
    L={}
    for r in csv.DictReader(open(c),delimiter='\t',quoting=csv.QUOTE_NONE):
        if r['level']=='5' and r['text'].strip():
            k=(r['block_num'],r['par_num'],r['line_num'])
            x,y,w,h=map(int,(r['left'],r['top'],r['width'],r['height']))
            if k not in L: L[k]=[x,y,x+w,y+h,[]]
            l=L[k]; l[0]=min(l[0],x);l[1]=min(l[1],y);l[2]=max(l[2],x+w);l[3]=max(l[3],y+h);l[4].append(r['text'])
    return sorted(L.values(),key=lambda l:l[1])
if __name__=='__main__':
    p=int(sys.argv[1])
    for i,l in enumerate(lines(p)): print(i,l[1],l[3],' '.join(l[4])[:60])
