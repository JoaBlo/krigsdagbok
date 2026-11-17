#!/usr/bin/env python3
"""Fyller i kolumnen "Förekomster" i namn.md automatiskt.

Kör:  python3 bygg_namn.py   (före bygg_index.py)

Varje rad i en tabell i namn.md som har en kolumn "Förekomster" och sökformer i backticks i
första kolumnen, t.ex. | `Blomqvist` `Blomquist` | … |, får Förekomster ersatt med alla
träffar i volymer/*/transkriptioner/NNN.md, som `10457/005:27`.
Rader utan backticks i första kolumnen lämnas orörda (förekomsterna förs då in för hand).

Sökningen görs i transkriptionens kodblock, rad för rad, sedan markeringar tagits bort
([ ] ? ⸌ ⸍ ~~), så att `Blomqvist` hittas även i [Blomqvist/Blomquist?]. Formen måste stå
som helt ord (inte inuti ett längre ord); en form som slutar med * är ett prefix
(`Illuk*` hittar Illukka, Illukan). Skiftläge spelar roll.
Ord som avstavats över radslut hittas inte – lägg i så fall till en sökform för delen.
"""
import re, pathlib

ROT = pathlib.Path(__file__).parent
NAMN = ROT / "namn.md"
ORD = r"0-9A-Za-zÅÄÖåäöÉéÜü"


def rader():
    """(volym, bild, radnr, text) för alla transkriberade rader."""
    for p in sorted((ROT / "volymer").glob("*/transkriptioner/[0-9]*.md")):
        t = p.read_text("utf-8")
        if "## Dubbelläsning" not in t:  # utkast räknas inte (samma spärr som bygg_index.py)
            continue
        m = re.search(r"^## Transkription\s*\n```\n(.*?)^```", t, re.M | re.S)
        if not m:
            continue
        for r in m.group(1).splitlines():
            mm = re.match(r"^(\d+)\s{2,}(.*)$", r)
            if mm:
                text = re.sub(r"~~|[\[\]?⸌⸍]", "", mm.group(2))
                yield p.parent.parent.name, p.stem, int(mm.group(1)), text


ALLA = list(rader())


def forekomster(former):
    trf = []
    for f in former:
        if f.endswith("*"):  # prefix: `Illuk*` hittar Illukka, Illukan, Illukasta
            rx = re.compile(rf"(?<![{ORD}]){re.escape(f[:-1])}")
        else:
            rx = re.compile(rf"(?<![{ORD}]){re.escape(f)}" + (rf"(?![{ORD}])" if f[-1] not in ".:" else ""))
        trf += [(v, b, n) for v, b, n, t in ALLA if rx.search(t)]
    trf = sorted(set(trf))
    return ", ".join(f"{v}/{b}:{n}" for v, b, n in trf) if trf else "–"


ut, kol, andrade = [], None, 0
for r in NAMN.read_text("utf-8").splitlines():
    if r.startswith("|"):
        c = [x.strip() for x in r.strip().strip("|").split("|")]
        if "Förekomster" in c:
            kol = c.index("Förekomster")
        elif kol is not None and not re.match(r"^\|[\s:|-]+\|?\s*$", r) and len(c) > kol:
            former = re.findall(r"`([^`]+)`", c[0])
            if former:
                ny = forekomster(former)
                if c[kol] != ny:
                    c[kol] = ny; andrade += 1
                r = "| " + " | ".join(c) + " |"
    else:
        kol = None
    ut.append(r)
NAMN.write_text("\n".join(ut) + "\n", "utf-8")
print(f"namn.md: {andrade} rader uppdaterade ({len(ALLA)} transkriberade rader genomsökta)")
