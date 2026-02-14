# Hva' er'd?

Der er swær at lave revytex. Det er med denne frække sag forhåbentligt lidt nememre at lave revytex. Det er IKKE en substitut for at bruge sin hjerne og tænke selv :)


## Hvor'n gør jeg?

`python main.py <path> [-o <output_path>]`

Programmet læser filen/filerne på `path` og outputter eventuelle fejl/mangler til terminalen (eller til `output_path` hvis `-o` er brugt).

Der outputtes i markdown format.

## Ka' du måske lig' vis' mig en eksempel eller to?

StangDennis vil gerne se fejl i filen `stangdenniss_sjove_sketch.tex`:

`python main.py ../revy/henrijeppes_sjove_sketch.tex`

Pastasalaten vil gerne se fejl i alle sine sketches opbevaret i mappen `hahaLolGRINERENstads` og have outputtet som en fil, da han har skrevet 3700 fisk, og det er lidt uoverskueligt i terminalen:

`python main.py ../revy/hahaLolGRINERENstads -o output.md`

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
