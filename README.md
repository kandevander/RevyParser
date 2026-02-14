# Hva er'd?

Der er swær at lave revytex. Det er med denne frække sag forhåbentligt lidt nememre at lave revytex. Det er IKKE en substitut for at bruge sin hjerne og tænke selv :)


## Hvor'n gør jeg?

`python main.py <path> [-o <output_path>]`

Programmet læser filen/filerne på `path` og outputter eventuelle fejl/mangler til terminalen (eller til `output_path` hvis `-o` er brugt).

Der outputtes i markdown format.

## Eksempler

StangDennis vil gerne se fejl i filen `stangdenniss_sjove_sketch.tex`:

`python main.py ../revy/henrijeppes_sjove_sketch.tex`

Pastasalaten vil gerne se fejl i alle sine sketches opbevaret i mappen `hahaLolGRINERENstads` og have outputtet som en fil, da han har skrevet 3700 fisk, og det er lidt uoverskueligt i terminalen:

`python main.py ../revy/hahaLolGRINERENstads -o output.md`


