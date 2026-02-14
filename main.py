import os
import re
import argparse
from pathlib import Path


class RevyParser:
    RE_CURLY = re.compile(r"{.*}") # Lidt dirty, da du i princippet kan have text i din \forscene{} uden at få fejl
    RE_CURLY_EMPTY = re.compile(r"{}")
    RE_LINEBREAK = re.compile(r"\\\\")
    RE_FORSCENE = re.compile(r"\\forscene")
    RE_FULDSCENE = re.compile(r"\\fuldscene")
    RE_SCENE = re.compile('(' + RE_FORSCENE.pattern + '|' + RE_FULDSCENE.pattern + ')')
    RE_PERFECT_SCENE = re.compile(RE_SCENE.pattern + RE_CURLY.pattern + RE_LINEBREAK.pattern)

    RE_PERSONGALLERI = re.compile(r'\\begin{Persongalleri}.*\\end{Persongalleri}', re.DOTALL)
    RE_ROLE_DECLARATION = re.compile(r'(\\sketchrolle)|(\\sangrolle)')
    RE_ILLEGAL_ROLE_DECL = re.compile('(' + RE_ROLE_DECLARATION.pattern + ')' + RE_CURLY.pattern)

    RE_ITEM = re.compile(r'\\item\s.+')
    RE_PAREN_ITEM = re.compile(r'\(.+?\)') # '?' is not greedy therefore matches closest parentheses
    
    RE_REKVISITTER = re.compile(r'\\begin{Rekvisitter}.*\\end{Rekvisitter}', re.DOTALL)

    RE_LYDEFFEKTER = re.compile(r'\\begin{Lydeffekter}.*\\end{Lydeffekter}', re.DOTALL)

    RE_TID = re.compile(r'\\tid{(\d{1,2}:\d{2})}')
    
    RE_BAND = re.compile(r'\\begin{Bandkommentar}(.*?)\\end{Bandkommentar}', re.DOTALL)
    
    
    RE_HASHTAG = re.compile(r'#')
    RE_COLON = re.compile(r':')
    RE_GAASEOEJNE = re.compile(r'[“”]')
    RE_BACKSLASH = re.compile(r'\\')
    RE_DOLLARSIGN = re.compile(r'\$')
    RE_PERCENT = re.compile(r'%')
    RE_SEMICOLON = re.compile(r';')
    RE_GAASEOEJNE = re.compile(r'[“”„"]')
    RE_BEGIN_SKETCH_OR_SANG = re.compile(
        r"\\begin\{(?:Sketch|Sang)}"  # Match Sketch or Sang
        r"(?:\[[^]]*])?" 
        r"\{([^}]*)}"
    )
    RE_BEGIN_STROFE = re.compile(
        r"\\begin\{Strofe}")

    def __init__(self, path):
        self.path = path
        self.lines = []
        self.content = ""
        self.errors: map[str, list[str]] = {} 
        for key in ["Header", "Rekvisitter", "Persongalleri", "Lydeffekter", "Sceneskift", "Diverse"]:
            self.errors[key] = []

    def validate(self):
        self._load_file()
        self.check_filename()
        self.check_title()
        self.check_tid()
        self.check_roles()
        self.check_band()
        self.check_lydeffekter()
        self.check_rekvisitter()
        self.check_scene_commands()
        self.check_strofe()


    def _load_file(self):
        with open(self.path, encoding="utf-8") as f:
            self.lines = f.readlines()
            self.content = "".join(self.lines)


    def check_filename(self):
        basename = os.path.basename(self.path)
        if " " in basename:
            self.errors["Header"].append(f"Filnavn indeholder mellemrum: {basename}")

    def check_title(self):
        for line in self.lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("%"):
                match = self.RE_BEGIN_SKETCH_OR_SANG.search(stripped)
                if match:
                    title = match.group(1)
                else:
                    title = stripped
                if self.RE_HASHTAG.search(title):
                    self.errors["Header"].append(f"Titel indeholder #: {title}")
                if self.RE_COLON.search(title):
                    self.errors["Header"].append(f"Titel indeholder kolon: {title}")
                if self.RE_BACKSLASH.search(title):
                    self.errors["Header"].append(f"Titel indeholder et backslash eller kommando: {title}")
                if self.RE_PERCENT.search(title):
                    self.errors["Header"].append(f"Titel indeholder et procenttegn: {title}")
                if self.RE_DOLLARSIGN.search(title):
                    self.errors["Header"].append(f"Titel indeholder et dollar tegn: {title}")
                if self.RE_SEMICOLON.search(title):
                    self.errors["Header"].append(f"Titel indeholder et semikolon: {title}")
                if self.RE_GAASEOEJNE.search(title):
                    self.errors["Header"].append(f"Titel indeholder gåseøjne: {title}")
                if title.lower() != os.path.splitext(os.path.basename(self.path))[0].lower():
                    self.errors["Header"].append(f"Titel og filnavn er ikke det samme: {title}")
                break

    def check_strofe(self):
        is_sketch = False
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith(r"\begin{Sketch}"):
                is_sketch = True
                break
        if not is_sketch:
            return
        if self.RE_BEGIN_STROFE.search(self.content):
            self.errors["Diverse"].append("Strofe-miljø fundet i sketch, det er ulovligt!. Sange med replikker SKAL TeX'es som en sang. Altså \begin{Sang}")


    def check_tid(self):
        match = self.RE_TID.search(self.content)
        if match:
            tid = match.group(1)
            if ":" not in tid:
                self.errros["Header"].append(f"Tidsformat ulovligt: {tid}")
        else:
            self.errors["Header"].append("Manglende eller ulovlig \\tid")

    def check_roles(self):
        roles, short_hands = [], []
        persongalleri = self.RE_PERSONGALLERI.search(self.content)


        if not persongalleri:
            self.errors["Persongalleri"].append("Der mangler et persongalleri. Fyfy!")
            return

        persongalleri = persongalleri.group()

        for item in self.RE_ITEM.findall(persongalleri):

            item = item.strip().lower()

            if not self.RE_ROLE_DECLARATION.search(item):
                self.errors["Persongalleri"].append(f"Manglende \\sketchrolle eller \\sangrolle i rollen: {item}")
            
            if self.RE_ILLEGAL_ROLE_DECL.search(item):
                self.errors["Persongalleri"].append(f"Ulovlig {{}} efter rolle type i {item}")

            name = item.strip('\\item ').split(' (')[0] #eww

            if name in roles:
                self.errors["Persongalleri"].append(f'Duplikeret rollenavn: {name}')

            if ',' in name:
                self.errors["Persongalleri"].append(f"Ulovligt komma i rollenavn: {name}")

            roles.append(name)

            # I assume the last paren_item is the role shorthand
            paren_items = self.RE_PAREN_ITEM.findall(item)

            if len(paren_items) == 0: 
                self.errors["Persongalleri"].append(f"Glemt rolle forkortelse for rollen: {item}")
                continue
            
            short_hand = paren_items[-1]

            if short_hand in short_hands:
                self.errors["Persongalleri"].append(f'Duplikeret rolle forkortelse: {short_hand}')

            short_hands.append(short_hand)

    def check_band(self):
        is_sang = False
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith(r"\begin{Sang}") or stripped.startswith(r"\begin{Sang}["):
                is_sang = True
                break

        if not is_sang:
            return

        matches = self.RE_BAND.findall(self.content)
        if not matches:
            self.errors["Header"].append("Sange SKAL have en bandkommentar")
        else:
            for match in matches:
                if not match.strip():
                    self.errors["Header"].append("Tomt bandkommentar-miljø")

    def check_lydeffekter(self):
        lydeffekter = self.RE_LYDEFFEKTER.search(self.content)

        if not lydeffekter: return

        lydeffekter = lydeffekter.group()

        items = self.RE_ITEM.findall(lydeffekter)
        if len(items) == 0: 
            self.errors["Lydeffekter"].append("Tomt lydeffekter environment. Hvis der ingen lydeffekter er, skal der ikke være noget environment")

    def check_rekvisitter(self):
        rekvisitter = self.RE_REKVISITTER.search(self.content)

        if not rekvisitter: return

        rekvisitter = rekvisitter.group()

        items = self.RE_ITEM.findall(rekvisitter)
        if len(items) == 0: 
            self.errors["Rekvisitter"].append("Tomt rekvisitter environment. Hvis der ingen rekvisitter er, skal der ikke være noget environment")
            return
        
        

        for item in items:
            if "(R)" not in item and "(P)" not in item:
                self.errors["Rekvisitter"].append(f"Rekvisit uden R/P markering: {item}")
        
        self.errors["Rekvisitter"].append("Vær opmærksom på, at dine rekvisitter har tydelige mål/dimensioner")

    def check_scene_commands(self):

        last_command, last_index = "", -1

        for i in range(len(self.lines)):
            line = self.lines[i].strip()
            if self.RE_SCENE.match(line):

                if self.RE_FULDSCENE.match(line) and self.RE_CURLY_EMPTY.search(line):
                    self.errors["Sceneskift"].append(f"Tom \\fuldscene{{}}. Overvej om der skal stå noget på scenen, og skriv det i krølleparenteserne. Linje {i+1}")

                if self.RE_FULDSCENE.match(line) and self.RE_FULDSCENE.match(last_command):
                    self.errors["Sceneskift"].append(f'Fuldscene -> fuldscene overgang fra linje {last_index+1} til linje {i+1}')

                if not self.RE_PERFECT_SCENE.fullmatch(line):
                    self.errors["Sceneskift"].append(f"Scenekommando skal slutte med {{}}\\\\ på linje {i+1}")


                prev, next = self.lines[i-1], self.lines[i+1]
                if not (prev == "\n" and next == "\n") :
                    self.errors["Sceneskift"].append(f"Der skal være blanke linjer over og under \\forscene{{}} eller \\fuldscene{{}} på linje {i+1}")

                last_command, last_index = line, i

        # Alt skal slutte på forscenen
        if not self.RE_FORSCENE.match(last_command):
            self.errors["Sceneskift"].append(f"Slutter ikke på forscenen")

def main():
    parser = argparse.ArgumentParser(description="Validate .tex file")
    parser.add_argument("path", nargs="+", help="Filenames or directory to check")
    args = parser.parse_args()
    should_print = True

    tex_files = []

    output = ""
    for path_str in args.path:
        path = Path(path_str)
        if path.is_file() and path.suffix == ".tex":
            tex_files.append(path)
        elif path.is_dir():
            tex_files.extend(path.glob("**/*.tex"))
        else:
            output += f"{path_str} er ikke en fil eller mappe\n"

        for f in tex_files:
            name = os.path.basename(f)
            output += f"# {name}\n"
            validator = RevyParser(f)
            validator.validate()

            for key, values in validator.errors.items():
                if len(values) == 0: continue

                output += f"\n### {key}\n"
                for val in values:
                    output += f"* {val}\n"

            output += "\n\n### Når du har rettet ovenstående er du næsten færdig. Så skal du bare\n"
            output += "* Checke at det compiler på overleaf/lokalt. Specielt på overleaf er det vigtigt at checke warnings!\n"
            output += "* Gennemgå LaTjeX listen under guides/revytex på drevet\n"
            output += "* (Optional) Bunde en bajer, alt efter hvor meget du mangler endnu :)\n"
            output += "\n\n---\n\n"
    
    if should_print: print(output)





if __name__ == "__main__":
    main()
