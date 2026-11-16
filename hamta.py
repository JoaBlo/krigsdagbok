#!/usr/bin/env python3
"""Hämtar bilder ur Kansallisarkistos digitaliserade arkiv (via Digihakemisto/Astia).

Användning
  python3 hamta.py                     hämtar allt som saknas enligt tabellen "Volymer" i CLAUDE.md
  python3 hamta.py <länk> [bilder]     lägger till länken i CLAUDE.md och hämtar
  python3 hamta.py --lista <länk> [sökord …]
                                       visar vad länken innehåller (volymerna i en samling,
                                       ev. bara de som innehåller sökorden), hämtar inget

<länk> kan vara
  https://digihakemisto.net/aineisto/2373598065            (en volym)
  https://digihakemisto.net/item/2373598065/6039587823/5   (en enskild bild – bild 5)
  https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373598065
  https://astia.narc.fi/uusiastia/viewer/?fileId=…&aineistoId=2373598065
[bilder] = alla | 5 | 1–10 | 3, 5, 12–20   (arkivets jaksonummer; standard: alla)

Resultat per volym (mappnamn = arkivets signum, t.ex. 10457):
  volymer/<signum>/bilder/NNN.jpg   NNN = jaksonumret i arkivet
  volymer/<signum>/kalla.md         titel, länkar och källhänvisning per bild
  volymer/<signum>/kalla.json       samma sak maskinläsbart
Bilder som redan finns hämtas inte igen.
"""
import datetime, html, json, pathlib, re, subprocess, sys, time

ROT = pathlib.Path(__file__).parent
CLAUDE = ROT / "CLAUDE.md"
DH = "https://digihakemisto.net"
UA = "tydda-texter/1.0 (transkriptionsprojekt)"


def get(url, fil=None):
    """Hämtar med curl (Pythons SSL-certifikat saknas på den här datorn)."""
    cmd = ["curl", "-sSL", "--fail", "--retry", "3", "-A", UA, url]
    if fil:
        subprocess.run(cmd + ["-o", str(fil)], check=True)
        return None
    return subprocess.run(cmd, check=True, capture_output=True).stdout.decode("utf-8", "replace")


def tolka_lank(lank):
    """→ (aineisto-id, bildspec som länken själv anger eller None)"""
    m = re.search(r"/item/(\d+)/\d+/(\d+)", lank)
    if m:
        return m.group(1), m.group(2)
    for p in (r"digihakemisto\.net/aineisto/(\d+)", r"[?&]aineistoId=(\d+)", r"kortti_aineisto\.html\?id=(\d+)"):
        m = re.search(p, lank)
        if m:
            return m.group(1), None
    sys.exit(f"Känner inte igen länken: {lank}")


def tolka_bilder(spec, finns):
    spec = (spec or "alla").strip().lower()
    if spec in ("", "alla"):
        return sorted(finns)
    ut = set()
    for del_ in re.split(r"\s*,\s*", spec):
        m = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", del_)
        if m:
            ut.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif del_.isdigit():
            ut.add(int(del_))
        elif del_:
            sys.exit(f"Förstår inte bildangivelsen '{del_}' (använd t.ex. alla, 5, 1–10, 3, 5, 12–20)")
    saknas = sorted(ut - set(finns))
    if saknas:
        print(f"  OBS: volymen har inga bilder med nummer {saknas} (finns 1–{max(finns)})")
    return sorted(ut & set(finns))


def las_volym(aid, filtret=()):
    s = get(f"{DH}/aineisto/{aid}")
    m = re.search(r"<title[^>]*>(.*?)</title>", s, re.S)
    titel = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else aid
    bilder = {int(n): fid for fid, n in re.findall(rf"/item/{aid}/(\d+)/(\d+)", s)}
    if not bilder:
        under = [(i, html.unescape(re.sub(r"\s+", " ", t)).strip()) for i, t in
                 re.findall(r'<a class="aineisto" href="/aineisto/(\d+)">\s*(?:<span[^>]*>)?([^<]+)', s)]
        if filtret:
            fras = re.sub(r"\s+", " ", " ".join(filtret)).lower()
            under = [(i, t) for i, t in under if fras in t.lower()]
        print(f"'{titel}' är ingen volym med bilder utan en samling. "
              + (f"Volymer som innehåller {' '.join(filtret)!r}:" if filtret else "Den innehåller:"))
        for i, t in under[:200]:
            print(f"  {DH}/aineisto/{i}   {t}")
        if len(under) > 200:
            print(f"  … och {len(under) - 200} till (filtrera: python3 hamta.py --lista <länk> JR 13)")
        sys.exit("Välj en volym ovan och lägg dess länk i CLAUDE.md.")
    m = re.match(r"^(.*?)\s+-\s+(\d+)\s+(.*)$", titel)
    signum = m.group(2) if m else aid
    return {"aineisto": aid, "titel": titel, "signum": signum, "bilder": bilder}


def astia_bild(aid, fid):
    return f"https://astia.narc.fi/uusiastia/viewer/?fileId={fid}&aineistoId={aid}"


def hamta(lank, spec):
    aid, egen = tolka_lank(lank)
    v = las_volym(aid)
    val = tolka_bilder(egen or spec, v["bilder"])
    mapp = ROT / "volymer" / v["signum"]
    (mapp / "bilder").mkdir(parents=True, exist_ok=True)
    w = max(3, len(str(max(v["bilder"]))))
    print(f"{v['signum']}: {v['titel']}\n  {len(v['bilder'])} bilder i volymen, {len(val)} valda")
    nya = 0
    for n in val:
        dst = mapp / "bilder" / f"{n:0{w}d}.jpg"
        if dst.exists() and dst.stat().st_size > 0:
            continue
        get(f"https://astia.narc.fi/uusiastia/ws/getFile.php?fileId={v['bilder'][n]}&aineistoId={aid}", dst)
        nya += 1
        print(f"  hämtade {dst.relative_to(ROT)}")
        time.sleep(1)  # var snäll mot arkivets server
    skriv_kalla(mapp, v, w)
    print(f"  {nya} nya bilder, {len(list((mapp / 'bilder').glob('*.jpg')))} totalt i {mapp.relative_to(ROT)}/bilder")
    return v


def skriv_kalla(mapp, v, w):
    """kalla.md/json: varifrån varje bild kommer. Källhänvisningen följer Digihakemistos egen
    mall (citation.js): '<titel>, jakso N; Kansallisarkisto: <Astia-länk> / Viitattu <datum>'."""
    gammal = {}
    if (mapp / "kalla.json").exists():
        gammal = {b["jakso"]: b for b in json.loads((mapp / "kalla.json").read_text("utf-8"))["bilder"]}
    idag = datetime.date.today()
    viitattu = f"{idag.day}.{idag.month}.{idag.year}"
    bilder = []
    for n, fid in sorted(v["bilder"].items()):
        fil = f"{n:0{w}d}.jpg"
        if not (mapp / "bilder" / fil).exists():
            continue
        g = gammal.get(n, {})
        url = astia_bild(v["aineisto"], fid)
        bilder.append({"jakso": n, "fil": fil, "fileId": fid, "astia": url,
                       "hamtad": g.get("hamtad", idag.isoformat()),
                       "viite": g.get("viite", f"{v['titel']}, jakso {n}; Kansallisarkisto: {url} / Viitattu {viitattu}")})
    data = {"titel": v["titel"], "signum": v["signum"], "aineisto": v["aineisto"],
            "digihakemisto": f"{DH}/aineisto/{v['aineisto']}",
            "astia": f"https://astia.narc.fi/uusiastia/kortti_aineisto.html?id={v['aineisto']}",
            "antal_i_volymen": len(v["bilder"]), "bilder": bilder}
    (mapp / "kalla.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), "utf-8")
    rader = [f"# {v['signum']} – källa", "",
             f"**Titel i arkivet:** {v['titel']}  ",
             f"**Arkiv:** Kansallisarkisto  ",
             f"**Digihakemisto:** {data['digihakemisto']}  ",
             f"**Astia:** {data['astia']}  ",
             f"**Bilder i volymen:** {len(v['bilder'])}, varav {len(bilder)} hämtade", "",
             "Skapad av hamta.py. Bildnumret (jakso) är arkivets eget, så `005.jpg` = jakso 5.", "",
             "| Bild | Original i Astia | Hämtad | Källhänvisning |", "|---|---|---|---|"]
    rader += [f"| {b['fil']} | [jakso {b['jakso']}]({b['astia']}) | {b['hamtad']} | {b['viite']} |" for b in bilder]
    (mapp / "kalla.md").write_text("\n".join(rader) + "\n", "utf-8")


def volymer_i_claude():
    t = CLAUDE.read_text("utf-8")
    sek = re.search(r"^## Volymer.*?\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    ut = []
    for r in (sek.group(1) if sek else "").splitlines():
        c = [x.strip() for x in r.strip().strip("|").split("|")]
        if r.startswith("|") and len(c) >= 2 and re.search(r"https?://", c[0]):
            ut.append((re.search(r"https?://\S+?(?=[)\s]|$)", c[0]).group(0), c[1]))
    return ut


def lagg_till_i_claude(lank, spec, titel):
    t = CLAUDE.read_text("utf-8")
    if lank in t:
        return
    sek = re.search(r"^## Volymer.*?\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    rader = sek.group(1).rstrip("\n").split("\n")
    sista = max(i for i, r in enumerate(rader) if r.startswith("|"))
    rader.insert(sista + 1, f"| {lank} | {spec or 'alla'} | {titel} |")
    t = t[:sek.start(1)] + "\n".join(rader) + "\n\n" + t[sek.end(1):].lstrip("\n")
    CLAUDE.write_text(t, "utf-8")
    print(f"  lade till raden i CLAUDE.md")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--lista":
        aid, _ = tolka_lank(a[1])
        v = las_volym(aid, a[2:])
        print(f"{v['signum']}: {v['titel']}\n  {len(v['bilder'])} bilder (jakso 1–{max(v['bilder'])})")
    elif a:
        lank, spec = a[0], " ".join(a[1:]) or None
        v = hamta(lank, spec)
        lagg_till_i_claude(lank, spec, v["titel"].split(" - ", 1)[-1])
    else:
        rader = volymer_i_claude()
        if not rader:
            print("Inga länkar i tabellen 'Volymer' i CLAUDE.md.")
        for lank, spec in rader:
            hamta(lank, spec)
