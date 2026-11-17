# Instruktion till översättare (finska → svenska)

Du översätter färdiga, dubbellästa transkriptioner av finska krigsdagbokssidor till svenska.
Du arbetar **bara med texten** i .md-filerna – du behöver inte titta på bilderna.

## Vilka filer
Samordnaren ger dig en lista med filer (`volymer/<signum>/transkriptioner/NNN.md`). Översätt bara de
rader som är på **finska**. Sidor som helt är på svenska hoppar du över (rapportera dem). Har filen redan
ett avsnitt `## Översättning (svenska)`, hoppa över den.

## Format
Lägg in avsnittet **direkt efter transkriptionens kodblock och dess notiser, före `## Osäkra passager`**:

````
## Översättning (svenska)
```
1  {sidnr: 25}
2  {marg: 18.10} På natten hade man patrullerat [Tekostetta?] från baksidan …
3  …
```
Översättning: Claude, utifrån den dubbellästa transkriptionen; ej granskad.
````

Regler:
1. **Samma radnummer** som i transkriptionen: en svensk rad per finsk rad. Rader som är på svenska i
   originalet (t.ex. på blandade sidor) utelämnas. Tomma eller rena siffer-/skissrader kan tas med oförändrade.
2. Översätt troget och sakligt, inte fritt. När finsk ordföljd kräver det får ett ord flyttas till grannraden;
   ett ord som avstavats över radslut översätts på den rad där det börjar.
3. Behåll `{marg: …}`, `{sidnr: …}`, `{skiss}`, `{tecken: …}`, `⸌…⸍` och `~~…~~` som de står (innehållet
   i `⸌…⸍` och `~~…~~` översätts).
4. Osäkra läsningar följer med: `[Tekostetta?]`, `[a/b?]`, `[oläsligt]` står kvar i översättningen.
   Är ett ord oläst i originalet är det oläst i översättningen också. Gissa aldrig fram innehåll som inte står.
5. **Egennamn** (personer, orter) och förbandsbeteckningar som "JR 61", "9K", "1AV" lämnas som i
   originalet ("Kamennyi Navolok", "maj. Bonde"). **Vanliga förkortningar översätts** till svensk
   motsvarighet eller förkortning, så att raden blir läsbar på svenska, t.ex.:
   Amp. = Sköt, vih. = fiendens/fienden, tyk. = art. (artilleri), krh. = grk. (granatkastare),
   pien. krh. = lätt grk., kran. = gran., kpl. = st., joukk. = pl. (pluton), kompp./K = komp.,
   patl. = bat., patl. kom. = bat.kom., kk = ksp. (kulspruta), pk = ksg. (kulsprutegevär),
   kiv. = gev., vänr. = fänr., luutn. = löjtn., kapt. = kapt., maj. = major, alik. = undersergeant,
   stm./sot. = soldat, Ilm. = Anmälde, Sää = Väder, vart. = vakt-, tied. = spanings-.
   Oklara förkortningar (t.ex. "psto", "M.K.", "tst.") lämnas kvar. Militära termer översätts med
   vedertagen svensk term (tukikohta = stödjepunkt, joukkue = pluton, komppania = kompani,
   kranaatinheitin = granatkastare, kenttävartio = fältvakt, korsu = korsu).
6. Är en översättning av ett ord osäker även när läsningen är säker, skriv den bästa översättningen och
   lägg en kort rad under blocket: "Rad 12: 'X' kan också betyda Y."
7. Ändra **ingenting** annat i filen (inte transkriptionen, inte andra avsnitt) och inga andra filer.

## Rapportera tillbaka (kort)
Vilka filer som fick översättning, vilka som hoppades över (helt svenska / redan översatta), och ev.
ord där översättningen är osäker.
