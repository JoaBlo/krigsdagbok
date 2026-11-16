#!/usr/bin/env python3
"""Bygger pages.json för webbvisaren (index.html).

Kör:  python3 bygg_index.py
Läser volymer/<signum>/kalla.json och volymer/<signum>/transkriptioner/NNN.md, namn.md och
ordlista.md och skriver pages.json med
  sidor      – metadata och transkriptionstext per transkriberad bild (nr = "10457/005")
  dokument   – en post per volym (volymvyn)
  kronologi  – sidorna i datumordning ur fältet "Datum på sidan" (tidslinjen)
  ordlista   – former och förklaringar ur ordlista.md (understrykning i texten)
Skapar också miniatyrer i volymer/<signum>/bilder/thumb/.
Kör om skriptet varje gång transkriptionerna, namn.md eller ordlista.md ändrats.
"""
import json, re, pathlib

ROT = pathlib.Path(__file__).parent
UT = ROT / "pages.json"
MARK = re.compile(r"\[[^\]]*\?\]|\[oläsligt\]|\[\.\.\.\]")


def kort(s, n=160):
    s = re.sub(r"\*\*|`", "", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def falt(t, namn):
    m = re.search(rf"^\*\*{namn}:\*\*\s*(.+?)\s*$", t, re.M)
    return re.sub(r"\s+$", "", m.group(1)) if m else ""


def iso(datum, ar_volym):
    """'30.6.[1941]' → '1941-06-30'; år saknas → volymens första år."""
    m = re.search(r"(\d{1,2})\s*\.\s*(\d{1,2})\s*\.?\s*\[?(\d{4})?", datum)
    if not m:
        return ""
    ar = m.group(3) or ar_volym
    return f"{ar}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if ar else ""


def volymordning():
    """Volymerna i samma ordning som tabellen i CLAUDE.md, övriga sist."""
    t = (ROT / "CLAUDE.md").read_text("utf-8") if (ROT / "CLAUDE.md").exists() else ""
    return re.findall(r"aineisto/(\d+)|aineistoId=(\d+)|kortti_aineisto\.html\?id=(\d+)|/item/(\d+)/", t)


ordning = ["".join(g) for g in volymordning()]
kallor = [json.loads(p.read_text("utf-8")) for p in (ROT / "volymer").glob("*/kalla.json")]
kallor.sort(key=lambda k: (ordning.index(k["aineisto"]) if k["aineisto"] in ordning else 999, k["signum"]))

sidor, dokument, kronologi = [], [], []
for k in kallor:
    sig = k["signum"]
    vmapp = ROT / "volymer" / sig
    m = re.search(r"\s+-\s+\d+\s+(.*)$", k["titel"])
    vtitel = re.sub(r"\s+\d{4}-\d{4}$", "", m.group(1) if m else k["titel"])
    ar_volym = (re.search(r"\b(19\d\d)\b", vtitel) or [None, ""])[1]
    perbild = {b["fil"].rsplit(".", 1)[0]: b for b in k["bilder"]}
    d = {"id": len(dokument), "signum": sig, "titel": vtitel, "astia": k["astia"],
         "digihakemisto": k["digihakemisto"], "antal": k["antal_i_volymen"],
         "hamtade": len(list((vmapp / "bilder").glob("*.jpg"))), "sidor": []}
    dokument.append(d)
    for p in sorted((vmapp / "transkriptioner").glob("[0-9]*.md")):
        t = p.read_text(encoding="utf-8")
        nr = p.stem
        b = perbild.get(nr, {})
        doktyp = falt(t, "Dokumenttyp")
        mm = re.search(r"^## Helhetsbedömning\s*\n+\s*\*\*Säkerhet:\s*([^*]+?)\.?\*\*", t, re.M)
        sak = re.sub(r"[.,;:]+$", "", mm.group(1).strip()) if mm else ""
        mm = re.search(r"^```\n(.*?)^```", t, re.M | re.S)
        block = mm.group(1) if mm else ""
        datum = falt(t, "Datum på sidan")
        s = {
            "nr": f"{sig}/{nr}", "vol": sig, "jakso": int(nr),
            "bild": f"volymer/{sig}/bilder/{nr}.jpg",
            "thumb": f"volymer/{sig}/bilder/thumb/{nr}.jpg",
            "fil": f"volymer/{sig}/transkriptioner/{nr}.md",
            "doktyp": kort(doktyp), "datum": datum, "sidnr": falt(t, "Sidnummer i dagboken"),
            "astia": b.get("astia", ""), "viite": b.get("viite", ""),
            # bilden direkt från Kansallisarkistos server (används på GitHub Pages, där bilderna inte finns)
            "fjarr": (f"https://astia.narc.fi/uusiastia/ws/getFile.php?fileId={b['fileId']}&aineistoId={k['aineisto']}"
                      if b.get("fileId") else ""),
            "sakerhet": sak, "rader": len([r for r in block.splitlines() if r.strip()]),
            "osakra": len(MARK.findall(block)),
            "dubbel": "## Dubbelläsning" in t, "rattad": "## Rättelser efter dubbelläsning" in t,
            "tredje": "## Tredje läsning" in t, "extern": "xtern källa" in t,
            "text": block, "dok": d["id"],
        }
        sidor.append(s)
        d["sidor"].append(s["nr"])
        sort = iso(datum, ar_volym)
        if sort:
            kronologi.append({"datum": datum, "handling": f"{sig} {vtitel}: {kort(doktyp, 90)}",
                              "kalla": s["nr"], "sort": sort})
kronologi.sort(key=lambda k: (k["sort"], k["kalla"]))

# miniatyrer (600 px) – skapas om de saknas eller är äldre än bilden
try:
    from PIL import Image, ImageOps
    for s in sidor:
        src, dst = ROT / s["bild"], ROT / s["thumb"]
        if src.exists() and (not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime):
            dst.parent.mkdir(exist_ok=True)
            im = ImageOps.exif_transpose(Image.open(src)); im.thumbnail((600, 800))
            im.convert("RGB").save(dst, quality=72, optimize=True)
except ImportError:
    print("Pillow saknas – miniatyrerna uppdaterades inte (pip install pillow)")


def md_tabellrader(text):
    """Alla datarader i markdown-tabeller som lista av cellistor (rubrikrader hoppas över)."""
    ut, rubrik = [], True
    for r in text.splitlines():
        if not r.startswith("|"):
            rubrik = True
            continue
        if re.match(r"^\|[\s:|-]+\|?\s*$", r):
            continue
        if rubrik:
            rubrik = False
            continue
        ut.append([c.strip() for c in r.strip().strip("|").split("|")])
    return ut


ordlista = []
p = ROT / "ordlista.md"
if p.exists():
    for c in md_tabellrader(p.read_text(encoding="utf-8")):
        if len(c) < 4:
            continue
        former = re.findall(r"`([^`]+)`", c[1])
        if former:
            ordlista.append({"ord": c[0], "former": former, "forklaring": c[2], "grund": c[3],
                             "exempel": c[4] if len(c) > 4 else ""})

data = {"sidor": sidor, "dokument": dokument, "kronologi": kronologi, "ordlista": ordlista}
UT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(dokument)} volymer, {len(sidor)} transkriberade sidor, {len(kronologi)} daterade, "
      f"{len(ordlista)} ord → {UT.name} ({UT.stat().st_size // 1024} kB)")
