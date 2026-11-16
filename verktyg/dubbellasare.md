# Instruktion till dubbelläsare

Du gör en oberoende andra läsning av osäkra ställen i en handskriven krigsdagbok. Du får av
samordnaren: volym (signum), en lista med ställen `NNN:rad` + vad som är osäkert, och en scratchpad-mapp.

**Läs inte** `volymer/<signum>/transkriptioner/` eller `namn.md`. Poängen är att du läser blint.

## Läsning
- Radnumrering: räkna rader av handskrift uppifrån; ett sidnummer som står på en egen rad räknas som
  egen rad. Samordnaren kan ge en ledtråd om var raderna finns (t.ex. marginaldatum).
- Utsnitt: `python3 verktyg/utsnitt.py tredjedelar volymer/<signum>/bilder/NNN.jpg <scratchpad>/dl/NNN`
- Zoom: `python3 verktyg/utsnitt.py zooma volymer/<signum>/bilder/NNN.jpg <scratchpad>/dl/NNN/zK.jpg x0 y0 x1 y1 [skala]`
- **Högst 2 inzoomningar per ställe.** Zooma gärna flera rader i ett utsnitt.
- Läs det som står; normalisera inte, översätt inte, gissa inte tyst. Markera `[ord?]`, `[a/b?]`, `[oläsligt]`.

## Rapportera tillbaka
En rad per ställe: `NNN:rad  <din läsning av hela raden>  — kort notering om vad som är osäkert`.
Ange om du är osäker på vilken rad som avses och vilken text du då antog var raden.
