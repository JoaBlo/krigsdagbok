#!/usr/bin/env python3
"""Bygger en fristående delningsversion av webbvisaren.

Mappen kan zippas och skickas/delas (OneDrive, Google Drive, USB …). Mottagaren
packar upp och dubbelklickar på "Oppna mig.html" – ingen webbserver, inget konto,
inget internet behövs.

Användning:  python3 bygg_delning.py [målmapp] [--max 2400] [--kvalitet 82]
Standard-målmapp: ~/Desktop/Krigsdagbok (delning)
Kör bygg_index.py först så att pages.json är aktuell.
"""
import argparse, glob, json, os, shutil, sys, zipfile
from PIL import Image, ImageOps

ROT = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("mal", nargs="?", default=os.path.expanduser("~/Desktop/Krigsdagbok (delning)"))
ap.add_argument("--max", type=int, default=2400, help="längsta bildsida i pixlar")
ap.add_argument("--kvalitet", type=int, default=82, help="JPEG-kvalitet")
ap.add_argument("--utan-zip", action="store_true", help="skapa inte <målmapp>.zip")
a = ap.parse_args()
mal = a.mal
os.makedirs(mal, exist_ok=True)

# 1. Data: pages.json + alla .md-filer som visaren läser, inbäddade i data.js
pages = json.load(open(os.path.join(ROT, "pages.json"), encoding="utf-8"))
files = {}
md = sorted(glob.glob(os.path.join(ROT, "volymer", "*", "transkriptioner", "*.md")))
md += sorted(glob.glob(os.path.join(ROT, "volymer", "*", "kalla.md")))
md += [os.path.join(ROT, f) for f in ("namn.md", "ordlista.md") if os.path.exists(os.path.join(ROT, f))]
for fn in md:
    rel = os.path.relpath(fn, ROT)
    files[rel] = open(fn, encoding="utf-8").read()
    os.makedirs(os.path.dirname(os.path.join(mal, rel)), exist_ok=True)
    shutil.copy2(fn, os.path.join(mal, rel))  # så att länken ".md-fil" fungerar
with open(os.path.join(mal, "data.js"), "w", encoding="utf-8") as f:
    f.write("window.EMBED = ")
    json.dump({"pages": pages, "files": files}, f, ensure_ascii=False)
    f.write(";\n")

# 2. Visaren
shutil.copy2(os.path.join(ROT, "index.html"), os.path.join(mal, "index.html"))
with open(os.path.join(mal, "Oppna mig.html"), "w", encoding="utf-8") as f:
    f.write('<!doctype html><meta charset="utf-8"><title>Krigsdagböcker</title>'
            '<meta http-equiv="refresh" content="0; url=index.html">'
            '<p><a href="index.html">Öppna Krigsdagböcker</a></p>\n')

# 3. Bilder (förminskade) och miniatyrer – bara för transkriberade sidor
n = 0
for s in pages["sidor"]:
    src, dst = os.path.join(ROT, s["bild"]), os.path.join(mal, s["bild"])
    if not os.path.exists(src):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        im.thumbnail((a.max, a.max), Image.LANCZOS)
        im.save(dst, "JPEG", quality=a.kvalitet, optimize=True, progressive=True)
        n += 1
    t = os.path.join(ROT, s["thumb"])
    if os.path.exists(t):
        os.makedirs(os.path.dirname(os.path.join(mal, s["thumb"])), exist_ok=True)
        shutil.copy2(t, os.path.join(mal, s["thumb"]))

with open(os.path.join(mal, "LAS MIG.txt"), "w", encoding="utf-8") as f:
    f.write("Krigsdagböcker – transkriptioner av krigsdagböcker ur Kansallisarkistos samlingar\n\n"
            "Så här öppnar du: dubbelklicka på \"Oppna mig.html\" (eller index.html). Sidan öppnas i webbläsaren.\n"
            "Ingen installation behövs. (Länkarna till originalen i Astia kräver internet.)\n\n"
            "Om du fått mappen som .zip: packa upp den först (högerklicka → Extrahera alla / dubbelklicka på Mac).\n")

# gamla filnamn med å/ä/ö tas bort
for gammal in ("Öppna mig.html", "LÄS MIG.txt"):
    for f in os.listdir(mal):
        import unicodedata
        if unicodedata.normalize("NFC", f) == gammal:
            os.remove(os.path.join(mal, f))

# zip-fil som fungerar på Windows: skapad med Python (inte Finder), utan __MACOSX och .DS_Store
if not a.utan_zip:
    zipnamn = mal.rstrip("/") + ".zip"
    bas = os.path.basename(mal.rstrip("/"))
    with zipfile.ZipFile(zipnamn, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, fs in os.walk(mal):
            for x in sorted(fs):
                if x == ".DS_Store" or x.startswith("._"):
                    continue
                full = os.path.join(d, x)
                rel = os.path.join(bas, os.path.relpath(full, mal))
                z.write(full, rel, compress_type=zipfile.ZIP_STORED if x.endswith(".jpg") else zipfile.ZIP_DEFLATED)
    print(f"Zip: {zipnamn} ({os.path.getsize(zipnamn)/1e6:.0f} MB) – skicka den här filen")

storlek = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(mal) for x in fs)
print(f"Klart: {mal}\n  {len(pages['sidor'])} sidor, {n} bilder förminskade nu, totalt {storlek/1e6:.0f} MB")
