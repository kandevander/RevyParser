# Hva' er'd?

Der er swær at lave revytex. Det er med denne frække sag forhåbentligt lidt nememre at lave revytex. Det er IKKE en substitut for at bruge sin hjerne og tænke selv :)


## Hvor'n gør jeg?

`python main.py <path> [-o <output_path>]`

Programmet læser filen/filerne på `path` og outputter eventuelle fejl/mangler til terminalen (eller til `output_path` hvis `-o` er brugt).

Der outputtes i markdown format.

## Ka' du måske lig' vis' mig en eksempel eller to?

StangDennis vil gerne se fejl i filen `stangdenniss_sjove_sketch.tex` og kører følgende kommando:

`python main.py revy/stangdenniss_sjove_sketch.tex`

Det giver følgende output i terminalen:

```
# stangdenniss_sjove_sketch.tex

### Header
* Titel og filnavn er ikke det samme: Nøgenløb på Aros

### Rekvisitter
* Rekvisit uden R/P markering: \item En kost
* Rekvisit uden R/P markering: \item Dildoen fra Husaren
* Vær opmærksom på, at dine rekvisitter har tydelige mål/dimensioner

### Persongalleri
* Manglende \sketchrolle eller \sangrolle i rollen: \item fuwq (f)
* Manglende \sketchrolle eller \sangrolle i rollen: \item stangdennis (f)
* Duplikeret rolle forkortelse: (f)

### Sceneskift
* Tom \fuldscene{}. Overvej om der skal stå noget på scenen, og skriv det i krølleparenteserne. Linje 21
* Fuldscene -> fuldscene overgang fra linje 21 til linje 27
* Scenekommando skal slutte med {}\\ på linje 29
* Der skal være blanke linjer over og under \forscene{} eller \fuldscene{} på linje 29


### Når du har rettet ovenstående er du næsten færdig. Så skal du bare
* Checke at det compiler på overleaf/lokalt. Specielt på overleaf er det vigtigt at checke warnings!
* Gennemgå LaTjeX listen under guides/revytex på drevet
* (Optional) Bunde en bajer, alt efter hvor meget du mangler endnu :)


---
```

Pastasalaten vil gerne se fejl i alle sine sketches opbevaret i mappen `hahaLolGRINERENstads` og have outputtet som en fil, da han har skrevet 3700 fisk, og det er lidt uoverskueligt i terminalen:

`python main.py revy/hahaLolGRINERENstads -o output.md`

Efter han har kørt kommandoen kan han finde outputtet i `output.md`

## TODO
* Ornli meget cleanup
* Online interface på tket.dk/revy
  * Evt. forsøge at compile det på prodekanus så der kan raporteres compile-fejl
* Pænere output i terminalen, da det er lidt yuck at se på markdown der ikke er renderet
* Bunde en bajer
* Nuke revytex og manus.py til grunden og starte helt forfra (ambitiøs)


## Jeg synes koden er grim/dårlig/kedelig/forkert 
Vi har kodet det med tømmermænd, forbedringer modtages med kyshånd <3

/HH & CERM24/25
