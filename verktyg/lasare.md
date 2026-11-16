# Instruktion till läsare (förstaläsning)

Du är en erfaren paleograf och transkriberar några sidor ur en krigsdagbok. Du får av samordnaren:
volym (signum), vilka bilder (NNN), scratchpad-mapp, och de sista raderna av sidan före din första bild.

## Läs först
- `CLAUDE.md`: avsnitten **Filens huvud**, **Regler för transkription** och **Förklaringar**.
- `namn.md`: kända personer, orter, förband, händer, förkortningar och konventioner
  (t.ex. `{marg: …}`, `{sidnr: N}`). Använd samma stavning som där när bilden stöder det.
- `volymer/<signum>/kalla.md`: titel, Astia-länk och källhänvisning för varje bild (till filhuvudet).
- En redan färdig fil i `volymer/<signum>/transkriptioner/` (om det finns) som mönster för formatet.

## Läsning
1. Gör tre utsnitt per sida:
   `python3 verktyg/utsnitt.py tredjedelar volymer/<signum>/bilder/NNN.jpg <scratchpad>/NNN`
   och läs dem med Read. Utskriften anger y-förskjutningen för varje utsnitt.
2. Zooma bara där det behövs:
   `python3 verktyg/utsnitt.py zooma volymer/<signum>/bilder/NNN.jpg <scratchpad>/NNN/zK.jpg x0 y0 x1 y1 [skala]`
   (originalkoordinater; ta gärna 2–4 rader eller en hel radhalva åt gången).
   **Högst 5 inzoomningar per sida, upp till 10 på mycket svåra sidor.** Går ordet inte att läsa
   efter det: markera `[ord?]`, `[a/b?]` eller `[oläsligt]` och gå vidare.
3. Är bilden vriden eller upp och ned: skriv det i din rapport (rätta den inte själv).

## Skriv
- En fil per bild: `volymer/<signum>/transkriptioner/NNN.md`, i exakt det format CLAUDE.md anger:
  filhuvud, `## Transkription` med kodblock, notiser, `## Osäkra passager` (tabell
  `| Rad | Bästa gissning | Varför |`), `## Helhetsbedömning` med `**Säkerhet: hög/medel/låg**` sist.
- Skriv "Kontrasten ökad i en arbetskopia (scratchpad) för att läsa." i filen.
- Skriv **inte** avsnittet "Dubbelläsning" och ändra **inga** andra filer (inte namn.md, ordlista.md,
  CLAUDE.md, bilder/).
- Förklaringar utan källa märks **Gissning (ingen källa)**. Inga omärkta förklaringar ur minnet.

## Rapportera tillbaka (kort)
1. Klara filer.
2. **Osäkra ställen för dubbelläsning:** en rad per ställe, `NNN:rad` och vad som är osäkert,
   men **utan din läsning** (t.ex. "005:27 efternamnet och initialerna efter Löjtn.").
3. **Nytt för namn.md:** personer, orter, förband, förkortningar och handkännetecken som inte redan
   finns där, med föreslagen sökform och `NNN:rad`.
4. Avvikelser (vriden bild, annan hand, bilaga, tom sida o.d.).
