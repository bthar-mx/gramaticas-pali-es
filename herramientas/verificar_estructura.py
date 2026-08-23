# -*- coding: utf-8 -*-
"""
Uso: python3 herramientas/verificar_estructura.py <borrador.md> <ini> <fin> <§desde> <§hasta>
Numeración triple, número del Saddanīti y llamadas de nota."""
import re, sys
import os, glob
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS=os.path.join(RAIZ,"docs")
FUENTE=(sys.argv[6] if len(sys.argv)>6
        else sorted(glob.glob(os.path.join(DOCS,"6*Kacc*.md")))[0])
path,ini,fin,a,b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
src="\n".join(open(FUENTE,encoding="utf-8").read().split("\n")[ini-1:fin])
bor=open(path,encoding="utf-8").read()
cuerpo=re.split(r"^## NOTAS DE NANDISENA",bor,flags=re.M)[0]

sf=[(int(x),int(y)) for x,y in re.findall(r"\*\*(\d+)\\\. (\d+)\\\.",src)]
sb=[(int(x),int(y)) for x,y in re.findall(r"^\*\*(\d+)\. (\d+)\.",cuerpo,re.M)]
print(f"suttas fuente {len(sf)} / borrador {len(sb)} | numeración triple idéntica: {sf==sb}")
if sf!=sb: print("  ", [z for z in zip(sf,sb) if z[0]!=z[1]][:6])
print(f"rango esperado §{a}–§{b}: {sb[0][0]==a and sb[-1][0]==b and len(sb)==b-a+1}")

def sad(txt,pat):
    return {int(m.group(1)): m.group(2) for m in re.finditer(pat,txt,re.S|re.M)}
ds=sad(src, r"\*\*(\d+)\\\..{0,400}?\((\d+(?:-\d+)?(?:, \d+(?:-\d+)?)*)\)")
db=sad(cuerpo, r"^\*\*(\d+)\. .{0,400}?\((\d+(?:-\d+)?(?:, \d+(?:-\d+)?)*)\)\.\*\*")
comunes=sorted(set(ds)&set(db))
malos=[(n,ds[n],db[n]) for n in comunes if ds[n]!=db[n]]
print(f"números del Saddanīti comparados: {len(comunes)} | discrepancias: {len(malos)} {malos[:5]}")
faltan=[n for n in range(a,b+1) if n not in db]
print(f"suttas sin número de Sad. en el borrador: {faltan}")

cs=sorted(int(x) for x in re.findall(r"\[\^(\d+)\]",re.sub(r"^\[\^\d+\]:.*$","",src,flags=re.M)))
cb=sorted(int(x) for x in re.findall(r"\[\^(\d+)\]",cuerpo))
print(f"llamadas de nota — fuente {cs}")
print(f"llamadas de nota — borrador {cb}")
print(f"idénticas: {cs==cb}")
defs=sorted(int(x) for x in re.findall(r"^\[\^(\d+)\]:",bor,re.M))
print(f"notas definidas en el borrador: {defs} | cubren las llamadas: {set(cb)<=set(defs)}")
