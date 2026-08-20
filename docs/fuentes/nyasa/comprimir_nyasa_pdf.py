#!/usr/bin/env python3
"""Recomprime el escaneo del Nyāsa (1933) a bitonal 200 dpi por tramos."""
import pymupdf, io, sys, os
from PIL import Image
SRC = "/mnt/user-data/uploads/Vimalbuddhi_-_Nyasa_path_1933.pdf"
a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
src = pymupdf.open(SRC)
dst = pymupdf.open()
for i in range(a, min(b, len(src))):
    pg = src[i]
    pix = pg.get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
    img = Image.frombytes("L", (pix.width, pix.height), pix.samples)
    bw = img.point(lambda x: 255 if x > 140 else 0, mode='1')
    buf = io.BytesIO(); bw.save(buf, "PNG", optimize=True)
    p = dst.new_page(width=pg.rect.width, height=pg.rect.height)
    p.insert_image(pg.rect, stream=buf.getvalue())
dst.save(out, deflate=True, garbage=3)
print(out, os.path.getsize(out)//1024//1024, "MB")
