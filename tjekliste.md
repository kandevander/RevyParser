# Tjekliste for aflevering af revy filer

Denne tjekliste samler ALLE krav til struktur, format og validering.
Gennemgå den for hver eneste fil du afleverer.

---

# Filnavn

- [ ] Filnavn matcher titel
- [ ] Underscore (_) bruges i stedet for mellemrum
- [ ] Kun tilladte postfixes bruges (_lang_version / _uden_hanne)

---

# Titel

- [ ] Ingen matematik ($, \mathbb{}, osv.)
- [ ] Ingen hashtag (#)
- [ ] Ingen kolon (:)
- [ ] Ingen TK-kommandoer eller specialmakroer (fx \CERM, \ikonINKA)
- [ ] Titel er ikke "Navn"

---

# Tid

- [x] \tid er angivet
- [x] Format er min:sek (fx 1:00)
- [x] Både minutter og sekunder er angivet
- [x] Tiden kan parses numerisk

---

# Kommandoer

- [ ] Starter med \fuldscene{}\\ eller \forscene{}\\
- [ ] Slutter med \forscene{}\\
- [ ] Der bruges altid \\ efter kommando
- [ ] Kommandoen står på sin egen linje
- [ ] Der er blank linje over og under scenekommando
- [ ] Eventuelle sceneopsætninger står i {} ved \fuldscene
- [ ] Sceneopsætning er også noteret i regibemærkning
- [ ] Der er mindst ét sceneskift
- [ ] Ingen fuldscene → fuldscene overgang (hverken internt eller mellem scener)

---

# Rolleliste

- [x] Mindst én rolle
- [x] Én rolle per \item
- [x] Ingen komma i rollenavn
- [x] Alle roller er unikke (case-insensitive)
- [x] Alle roller har \sketchrolle eller \sangrolle
- [ ] Ingen {} efter \sketchrolle / \sangrolle
- [ ] Kønsmarkering (\dreng / \pige) bruges korrekt
- [ ] Ingen rolle har både \dreng og \pige
- [ ] Dans er tydeligt angivet hvis relevant

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

