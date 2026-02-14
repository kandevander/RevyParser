# Tjekliste for aflevering af revy filer

Denne tjekliste samler ALLE krav til struktur, format og validering.
Gennemgå den for hver eneste fil du afleverer.

---

# Filnavn

- [x] Filnavn matcher titel
- [x] Underscore (_) bruges i stedet for mellemrum
- [x] Kun tilladte postfixes bruges (_lang_version / _uden_hanne)

---

# Titel

- [x] Ingen matematik ($, \mathbb{}, osv.)
- [x] Ingen hashtag (#)
- [x] Ingen kolon (:)
- [x] Titel er ikke "Navn"

---

# Tid

- [x] \tid er angivet
- [x] Format er min:sek (fx 1:00)
- [x] Både minutter og sekunder er angivet
- [x] Tiden kan parses numerisk

---

# Kommandoer

- [x] Starter med \fuldscene{}\\ eller \forscene{}\\
- [x] Slutter med \forscene{}\\
- [x] Der bruges altid \\ efter kommando
- [x] Kommandoen står på sin egen linje
- [x] Der er blank linje over og under scenekommando
- [x] Eventuelle sceneopsætninger står i {} ved \fuldscene
- [ ] Sceneopsætning er også noteret i regibemærkning
- [ ] Ingen fuldscene → fuldscene overgang (hverken internt eller mellem scener)

---

# Rolleliste

- [x] Mindst én rolle
- [x] Én rolle per \item
- [x] Ingen komma i rollenavn
- [x] Alle roller er unikke (case-insensitive)
- [x] Alle roller har \sketchrolle eller \sangrolle
- [x] Ingen {} efter \sketchrolle / \sangrolle

---

# Sange

- [ ] Der er altid bandkommentar
- [ ] Ingen typografiske gåseøjne (“ ”)
- [ ] Sketch med sang er tex’et som sang

---

# Lydeffekter

- [ ] Ingen lydeffekter-environment hvis der ingen er
- [ ] Der bruges \lyd (ikke \Lyd)

---

# Rekvisitter

- [ ] Ingen rekvisit-environment hvis der ingen er
- [ ] Alle rekvisitter er markeret (R) eller (P)
- [ ] Beskrivelser er selvforklarende

---

# Footer

- [ ] Kun navne/kammernavne (ikke "Credits:")
- [ ] \TKprefix{} bruges korrekt

---

# Generelt

- [ ] Ingen fancy TeX
- [ ] Ingen nye pakker importeres
- [ ] Filen compiler uden fejl
- [ ] OverLeaf warnings/errors er tjekket
- [ ] Filen er uploadet korrekt sted

---

# Kritiske fejl (stopper build)

- [ ] Forkert filnavn
- [ ] Kolon i titel
- [ ] Manglende \tid
- [ ] Ugyldigt tidsformat
- [ ] Manglende bandkommentar i sang
- [ ] Ingen roller
- [ ] Duplikatroller
- [ ] Import af pakker
- [ ] Manglende start/slut \fuldscene/\forscene
- [ ] Fuldscene → fuldscene overgang

---

