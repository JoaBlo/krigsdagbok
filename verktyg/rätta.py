#!/usr/bin/env python3
"""Inför beslut efter dubbelläsning i en transkription.

  python3 verktyg/rätta.py <fil.md> <beslut.json>

beslut.json: {"rader": {"12": "ny radtext", …},
              "osakra": {"12": "| 12 | gissning | varför |", …},   # ersätter/lägger till rader i Osäkra passager
              "dubbel": ["| 12 | första | andra | beslut |", …],    # rader i tabellen under ## Dubbelläsning
              "dubbel_text": "fri text efter tabellen (valfri)",
              "sakerhet": "medel"}                                    # valfri
Raderna i Osäkra passager vars Rad-kolumn omfattar en nyckel (även "7–8", "15, 21") tas bort
innan de nya läggs till.
"""
import json, re, sys, datetime


def rader_i(s):
    """Radnumren som en cell eller nyckel omfattar: "12", "7–8", "3, 52", "9–10, 14"."""
    nr = set()
    for part in re.split(r"\s*,\s*", s.strip()):
        m = re.match(r"^(\d+)\s*[–-]\s*(\d+)$", part)
        if m:
            nr.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            nr.add(int(part))
    return nr


def omfattar(cell, key):
    return bool(rader_i(cell) & rader_i(key))


fil, bes = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
t = open(fil, encoding="utf-8").read()
for k, v in bes.get("rader", {}).items():
    t, n = re.subn(rf"^{k}  .*$", lambda m: f"{k}  {v}", t, count=1, flags=re.M)
    assert n == 1, f"rad {k} saknas i {fil}"
if bes.get("osakra"):
    i = t.index("## Osäkra passager"); j = t.index("\n## ", i + 5)
    sek = t[i:j].rstrip("\n").split("\n")
    keep = [r for r in sek if not (r.startswith("| ") and not r.startswith("| Rad") and
            any(omfattar(r.split("|")[1], k) for k in bes["osakra"]))]
    keep += list(bes["osakra"].values())
    t = t[:i] + "\n".join(keep) + "\n" + t[j:]
if bes.get("dubbel"):
    blk = ("## Dubbelläsning\nOberoende läsare (utan att ha sett transkriptionen), "
           f"{datetime.date.today()}. Avvikande läsningar:\n\n| Rad | Första läsningen | Andra läsningen | Beslut |\n|---|---|---|---|\n"
           + "\n".join(bes["dubbel"]) + "\n" + (("\n" + bes["dubbel_text"] + "\n") if bes.get("dubbel_text") else "") + "\n")
    t = t.replace("## Helhetsbedömning", blk + "## Helhetsbedömning", 1)
if bes.get("sakerhet"):
    t = re.sub(r"^\*\*Säkerhet:[^*]*\*\*", f"**Säkerhet: {bes['sakerhet']}**", t, flags=re.M)
open(fil, "w", encoding="utf-8").write(t)
print("ok", fil)
