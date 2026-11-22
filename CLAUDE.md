# Transkription av krigsdagböcker

## Volymer
En rad per volym. **Länk** = volymens sida i Digihakemisto (`digihakemisto.net/aineisto/…`),
en enskild bild (`digihakemisto.net/item/…`) eller Astia (`astia.narc.fi/…?id=…`).
**Bilder** = `alla`, ett nummer `5`, ett intervall `1–10` eller en lista `3, 5, 12–20`
(arkivets bildnummer, "jakso"). **Anm.** kan lämnas tom – den fylls i med volymens titel
när bilderna hämtas. Lägg till en rad och skriv "hämta och transkribera",
eller kör `python3 hamta.py <länk> [bilder]` så läggs raden till automatiskt.
Är länken en samling i stället för en volym listar hamta.py volymerna i den.

| Länk | Bilder | Anm. |
|---|---|---|
| https://digihakemisto.net/aineisto/2373598065 | alla | 10457 Jalkaväkirykmentti 13. 1. komppania, 12.6.1941 - 18.10.1941 1941-1941 |
| https://digihakemisto.net/aineisto/2373598920 | alla | 10458 Jalkaväkirykmentti 13. 1. komppania, 19.10.1941 - 22.12.1941 1941-1941 |
| https://digihakemisto.net/aineisto/2373599907 | alla | 10459 Jalkaväkirykmentti 13. 1. komppania, 23.12.1941 - 21.4.1942 1941-1942 |
| https://digihakemisto.net/aineisto/2373600894 | alla | 10460 Jalkaväkirykmentti 13. 1. komppania, 22.4.1942 - 17.6.1942 1942-1942 |
| https://digihakemisto.net/aineisto/2373601513 | alla | 10461 Jalkaväkirykmentti 13. 1. komppania, 18.6.1942 - 31.7.1943 1942-1943 |
| https://digihakemisto.net/aineisto/2373603603 | alla | 10462 Jalkaväkirykmentti 13. 1. komppania, 1.8.1943 - 13.7.1944 1943-1944 |
| https://digihakemisto.net/aineisto/2373594060 | alla | 10454 Jalkaväkirykmentti 13. Esikunta, 1.1.1944 - 23.5.1944 1944-1944 |
| https://digihakemisto.net/aineisto/2373595137 | alla | 10455 Jalkaväkirykmentti 13. Esikunta, 24.5.1944 - 21.8.1944 1944-1944 |
| https://digihakemisto.net/aineisto/2373596178 | alla | 10456 Jalkaväkirykmentti 13. Esikunta - |
| https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373589045 | alla | 10449 Jalkaväkirykmentti 13. Esikunta, 15.6.1941 - 7.9.1941 1941-1941 |
| https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373589846 | alla | 10450 Jalkaväkirykmentti 13. Esikunta, 13.9.1941 - 5.2.1942 1941-1942 |
| https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373591055 | alla | 10451 Jalkaväkirykmentti 13. Esikunta, 6.2.1942 - 23.4.1942 1942-1942 |
| https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373592230 | alla | 10452 Jalkaväkirykmentti 13. Esikunta, 24.4.1942 - 17.10.1942 1942-1942 |
| https://astia.narc.fi/uusiastia/kortti_aineisto.html?id=2373593405 | alla | 10453 Jalkaväkirykmentti 13. Esikunta, 18.10.1942 - 7.1.1943 1942-1943 |


## Kontext
- Typ av dokument: krigsdagböcker (sotapäiväkirjat) ur Kansallisarkistos samlingar, ca 1939–1945
- Språk: svenska och finska. Transkribera på originalspråket. Sidor (eller delar av sidor) på finska får
  dessutom en svensk översättning i avsnittet `## Översättning (svenska)` direkt efter transkriptionen
  (se Regler 9).
- Skrift: ofta blyerts på rutat papper, snabb handstil, militära förkortningar,
  datum och klockslag i vänstermarginalen.
- Namn som förekommer: se namn.md.

## Mappar
- `volymer/<signum>/bilder/` – bilderna, `NNN.jpg` där NNN = arkivets jaksonummer
  (hämtas med hamta.py; finns inte i git eftersom de alltid kan hämtas på nytt)
- `volymer/<signum>/transkriptioner/` – en .md-fil per bild (`005.jpg` → `005.md`)
- `volymer/<signum>/kalla.md` – titel, arkivlänkar och källhänvisning per bild (skapas av hamta.py)
- `namn.md` – personer, orter, förband, skrivarhänder, förkortningar (gemensam för alla volymer)
- `ordlista.md` – förklaringar av ord och förkortningar, med källa
- `beslut.md` – min privata logg, ligger inte i git (repot är publikt)
- `verktyg/utsnitt.py` – kontrastförstärkta utsnitt (tredjedelar) och inzoomning för läsning
- `verktyg/lasare.md`, `verktyg/dubbellasare.md` – instruktionerna till läsarna i en omgång
- `verktyg/oversattare.md` – instruktion för den svenska översättningen av finska sidor
- `verktyg/rätta.py` – för in besluten efter dubbelläsning (rader, osäkra passager, avsnittet Dubbelläsning)
- `bygg_namn.py` – fyller i "Förekomster" i namn.md ur transkriptionerna

## Hänvisningar
`10457/005:12` = volym 10457, bild (jakso) 5, rad 12. Inom samma volym räcker `005:12`.

## Arbetssätt
Du är en erfaren paleograf. Gå igenom volymerna i tabellens ordning och bilderna i nummerordning.
1. Kör `python3 hamta.py` så att alla bilder i tabellen finns lokalt.
2. Hoppa över bilder som redan har en .md-fil.
3. Läs namn.md innan du börjar. Där finns personer, orter, förband, skrivarhänder,
   lösta förkortningar och konventioner. För in nya namn, orter, förband, händer och
   förkortningar i namn.md med sökformer i backticks (alla stavningar som förekommer).
   Förekomsterna (`volym/bild:rad`) fylls i av `python3 bygg_namn.py`.
4. Efter varje omgång (se Omgångar) dubbelläser en annan läsare de osäkra passagerna utan att ha sett
   transkriptionen. Avvikande läsningar antecknas i filen under rubriken "Dubbelläsning".
5. Är bilden vriden, rätas den upp och sparas rättvänd. Originalet kan alltid hämtas
   igen via länken i kalla.md.
6. Blek blyerts: det är tillåtet att öka kontrasten i en arbetskopia för att läsa
   (i scratchpad, inte i bilder/; `verktyg/utsnitt.py`). Notera i filen om det gjorts.
7. Logga beslut i beslut.md i stället för att stanna och fråga.

## Filens huvud
Varje transkription börjar så här (fälten används av webbvisaren):

```
# 10457 – bild 005

**Volym:** <titel ur kalla.md>
**Original:** <Astia-länk ur kalla.md>
**Källhänvisning:** <ur kalla.md>
**Sidnummer i dagboken:** <det som står på sidan, eller "saknas">
**Datum på sidan:** <t.ex. 30.6.[1941]; år inom [] om det inte står på sidan>
**Dokumenttyp:** <t.ex. Krigsdagbok, löpande text / Bilaga: order / Pärm>
**Hand:** <skrivarhand enligt namn.md>
```

## Regler för transkription
1. Återge texten exakt som den står. Behåll stavning, förkortningar, radbrytningar och
   överstrykningar (~~text~~). Modernisera inte och översätt inte i transkriptionen.
2. Numrera varje rad (1, 2, 3 …) så att numreringen motsvarar originalets rader.
   Slå aldrig ihop rader. Transkriptionen står i ett kodblock (```) under rubriken
   `## Transkription`, en rad per originalrad: radnummer, två mellanslag, text.
3. Det som står i vänstermarginalen (datum, klockslag) skrivs först på den rad det står
   vid, inom `{marg: …}`, t.ex. `1  {marg: 30.6.} Men nu blev det ändå tid …`
4. Markera osäkerhet i texten:
   - [ord?] = osäker läsning
   - [ord1/ord2?] = två möjliga läsningar
   - [oläsligt] = går inte att läsa
   - [...] = skadad eller saknad text
   - ⸌ord⸍ = tillagt ovanför raden (eller med insättningstecken) av skrivaren;
     läses in där det står
5. Gissa aldrig tyst. Markera hellre osäkerhet än att skriva något som ser säkert ut.
6. Under transkriptionen i samma fil: lista osäkra passager med radnummer,
   bästa gissning och varför du är osäker.
7. Sist i filen: `## Helhetsbedömning` och `**Säkerhet: hög/medel/låg**`.
8. Extern källa (ordböcker, förkortningslistor, matriklar, andra arkiv m.m.): skriv alltid
   "Extern källa:", källans namn, post-ID eller URL och vad den stöder.
   Externa uppgifter förs aldrig in omarkerade i transkriptionen.
9. Finska sidor: under transkriptionen (före `## Osäkra passager`) ett avsnitt `## Översättning (svenska)`
   med ett kodblock med **samma radnummer** som transkriptionen, en svensk rad per finsk rad
   (svenska rader i originalet utelämnas). Osäkra läsningar följer med som `[ord?]`, `{marg: …}` och
   `{skiss}` behålls, egennamn och förkortningar lämnas oöversatta. Under blocket:
   "Översättning: Claude, utifrån den dubbellästa transkriptionen; ej granskad." Instruktion:
   `verktyg/oversattare.md`. Översättningen görs efter dubbelläsningen.

## Förklaringar: länka, annars märkt gissning
- Varje förklaring (av förkortningar, ord, grader, förband, platser) ska om möjligt ha en
  källa med länk och ett ordagrant citat som kontrollerats mot den hämtade sidan.
- Finns ingen källa får en förklaring skrivas, men den ska märkas
  **Gissning (ingen källa)** och det ska framgå vad gissningen bygger på
  (t.ex. "sammanhanget i 005:12").
- Omärkta förklaringar ur eget minne är inte tillåtna.

## Webbvisaren
- `python3 bygg_index.py` – bygger pages.json och miniatyrer (kör efter varje ändring).
- Titta lokalt: `python3 -m http.server` i projektmappen → http://localhost:8000
- På GitHub Pages finns inga bilder i repot; visaren hämtar dem då direkt från Astia
  (fältet `fjarr` i pages.json).
- `python3 bygg_delning.py` – fristående kopia i ~/Desktop/Krigsdagbok (delning) som kan
  zippas och öppnas med dubbelklick på "Öppna mig.html".
- Osäkra passager listas i en tabell `| Rad | Bästa gissning | Varför |` under rubriken
  `## Osäkra passager`; då visas motiveringen vid raden i visaren.

## Omgångar
- En omgång = **10–20 bilder** i följd (normalt 15). En omgång slutar alltid vid volymens slut, så att
  varje commit bara gäller en volym (sista omgången i en volym kan alltså vara kortare).
- "kör" = kör omgång efter omgång i tabellens ordning tills allt är klart eller användaren säger stopp.
- Ordningen i varje omgång:
  1. **Förstaläsning, parallellt:** dela omgången i 3 block om ca 5 bilder i följd och starta en
     läsare (hjälpagent) per block med instruktionen i `verktyg/lasare.md`. Ge varje läsare volym,
     bilder, scratchpad-mapp och de sista raderna av sidan före blocket.
  2. **Dubbelläsning:** en ny läsare med `verktyg/dubbellasare.md` får alla osäkra ställen
     (`NNN:rad` + vad som är osäkert, utan förstaläsningen).
  3. **Avgörande:** jämför läsningarna; titta själv i bilden där de skiljer sig. Rätta, eller sätt
     båda alternativen `[a/b?]`. Skriv avsnittet `## Dubbelläsning` (tabell: Rad | Första läsningen |
     Andra läsningen | Beslut) i varje fil.
  4. **Översättning:** för finska sidor i omgången, en översättare (hjälpagent, bara text) med
     `verktyg/oversattare.md`.
  5. För in nytt i namn.md (sökformer, roll, anm.); kör `python3 bygg_namn.py` och
     `python3 bygg_index.py`.
  6. Kontrollera `git status`, committa med meddelandet "10457: Transkription 006–020"
     (rätt volym och nummer) och pusha.
- Läsbudget: 3 utsnitt + högst 5 inzoomningar per sida (10 på mycket svåra sidor); dubbelläsaren
  högst 2 per ställe. Hellre `[ord?]` än fler inzoomningar.
- Ordlistan (ordlista.md, med kontrollerade källor och citat) görs som ett eget pass när en volym är
  klar, inte i varje omgång.
- För att spara tokens: starta gärna en ny session (`/clear`) mellan omgångarna; allt som behövs
  finns i filerna.
- **Pusha aldrig före dubbelläsningen.** Det som syns på webbsidan ska vara dubbelläst,
  inte ett första utkast.
- Bilderna pushas aldrig (de ligger i .gitignore); det som pushas är .md-filerna,
  namn.md, ordlista.md och pages.json.

**Repot JoaBlo/krigsdagbok är publikt** och visas som webbsida via GitHub Pages
(https://joablo.github.io/krigsdagbok/). Allt som pushas syns direkt för alla och finns kvar
i historiken. Därför:
- beslut.md och bilderna ska aldrig in i git (de står i .gitignore – ändra inte det);
- kontrollera `git status` före varje commit så att inga oavsiktliga filer följer med.
