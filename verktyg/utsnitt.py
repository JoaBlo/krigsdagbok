#!/usr/bin/env python3
"""Arbetskopior för läsning (kontrastförstärkta). Skriv dem i scratchpad, aldrig i bilder/.

  python3 verktyg/utsnitt.py tredjedelar <bild.jpg> <utmapp>
      → <utmapp>/<NNN>_1.jpg, _2.jpg, _3.jpg: övre, mellersta och nedre tredjedelen i full
        upplösning med lite överlapp. Utskriften anger varje utsnitts y-förskjutning, så att
        en punkt (x, y) i utsnitt k motsvarar (x, y + förskjutning) i originalet.

  python3 verktyg/utsnitt.py zooma <bild.jpg> <ut.jpg> x0 y0 x1 y1 [skala]
      → en ruta ur originalet (originalkoordinater), kontrastförstärkt och förstorad (standard 1.5).
"""
import sys, pathlib
from PIL import Image, ImageOps


def tredjedelar(src, utmapp):
    im = Image.open(src).convert("L")
    w, h = im.size
    ut = pathlib.Path(utmapp); ut.mkdir(parents=True, exist_ok=True)
    stam = pathlib.Path(src).stem
    for i in range(3):
        y0 = max(0, int(h * i / 3) - 60); y1 = min(h, int(h * (i + 1) / 3) + 60)
        c = ImageOps.autocontrast(im.crop((0, y0, w, y1)), cutoff=1)
        p = ut / f"{stam}_{i + 1}.jpg"
        c.save(p, quality=88)
        print(f"{p}  y-förskjutning {y0}  ({w}x{y1 - y0})")


def zooma(src, ut, x0, y0, x1, y1, skala=1.5):
    im = Image.open(src).convert("L").crop((int(x0), int(y0), int(x1), int(y1)))
    im = ImageOps.autocontrast(im, cutoff=1)
    im = im.resize((int(im.width * float(skala)), int(im.height * float(skala))), Image.LANCZOS)
    pathlib.Path(ut).parent.mkdir(parents=True, exist_ok=True)
    im.save(ut, quality=90)
    print(ut)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "tredjedelar":
        tredjedelar(a[1], a[2])
    elif len(a) in (7, 8) and a[0] == "zooma":
        zooma(*a[1:])
    else:
        sys.exit(__doc__)
