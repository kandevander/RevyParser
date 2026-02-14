import os
import re
import argparse


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
    
    
    #RE_ITEM = re.compile(r'\\item\s.+\s\(.+\)\s(?:\\sketchrolle|\\sangrolle)')

    RE_TID = re.compile(r'\\tid{(\d{1,2}:\d{2})}')
    
    RE_BAND = re.compile(r'\\begin{Bandkommentar}(.*?)\\end{Bandkommentar}', re.DOTALL)
    RE_LYDEFFEKTER = re.compile(r'\\lyd{(.+?)}')
    RE_REKVISITTER = re.compile(r'\\begin{(Rekvisitter)}(.*?)\\end{\1}', re.DOTALL)
    RE_HASHTAG = re.compile(r'#')
    RE_COLON = re.compile(r':')
    RE_GAASEOEJNE = re.compile(r'[“”]')
    RE_BACKSLASH = re.compile(r'\\')
    RE_DOLLARSIGN = re.compile(r'\$')
    RE_PERCENT = re.compile(r'%')
    RE_SEMICOLON = re.compile(r';')
    RE_GAASEOEJNE = re.compile(r'[“”„"]')
    RE_BEGIN_SKETCH = re.compile(r"\\begin\{Sketch}\{([^}]*)}")

    def __init__(self, path):
        self.path = path
        self.lines = []
        self.content = ""

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


    def _load_file(self):
        with open(self.path, encoding="utf-8") as f:
            self.lines = f.readlines()
            self.content = "".join(self.lines)


    def check_filename(self):
        basename = os.path.basename(self.path)
        if " " in basename:
            print(f"[FILNAVN] Filnavn indeholder mellemrum: {basename}")

    def check_title(self): #TODO ensure this is also checked for songs
        for line in self.lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("%"):
                match = self.RE_BEGIN_SKETCH.search(stripped)
                if match:
                    title = match.group(1)
                else:
                    title = stripped
                if self.RE_HASHTAG.search(title):
                    print(f"[TITEL] Titel indeholder #: {title}")
                if self.RE_COLON.search(title):
                    print(f"[TITEL] Titel indeholder kolon: {title}")
                if self.RE_BACKSLASH.search(title):
                    print(f"[TITEL] Titel indeholder et backslash eller kommando {title}")
                if self.RE_PERCENT.search(title):
                    print(f"[TITEL] Titel indeholder et procenttegn {title}")
                if self.RE_DOLLARSIGN.search(title):
                    print(f"[TITEL] Titel indeholder et dollar tegn {title}")
                if self.RE_SEMICOLON.search(title):
                    print(f"[TITEL] Titel indeholder et semikolon {title}")
                if self.RE_GAASEOEJNE.search(title):
                    print(f"[TITEL] Titel indeholder gåseøjne {title}")
                if title == "navn":
                    print(f"[TITEL] Titel er ugyldig: {title}")
                if title.lower() != os.path.splitext(os.path.basename(self.path))[0].lower():
                    print(f"[TITEL] Titel og filnavn er ikke det samme {title}")
                break

    def check_tid(self):
        match = self.RE_TID.search(self.content)
        if match:
            tid = match.group(1)
            if ":" not in tid:
                print(f"[TID] Tidsformat ugyldigt: {tid}")
        else:
            print("[TID] Manglende \\tid")

    def check_roles(self):
        roles, short_hands = [], []
        persongalleri = self.RE_PERSONGALLERI.search(self.content)


        if not persongalleri:
            print("Der mangler et persongalleri. Fyfy!")
            return

        persongalleri = persongalleri.group()

        for item in self.RE_ITEM.findall(persongalleri):
            #print(item)

            item = item.strip().lower()

            if not self.RE_ROLE_DECLARATION.search(item):
                print(f"Manglende \\sketchrolle eller \\sangrolle i rollen: {item}")
            
            if self.RE_ILLEGAL_ROLE_DECL.search(item):
                print(f"Ulovlig {{}} efter rolle type i {item}")

            name = item.strip('\\item ').split(' (')[0] #eww

            if name in roles:
                print(f'Duplikeret rollenavn: {name}')

            if ',' in name:
                print(f"Ulovligt komma i rollenavn: {name}")

            roles.append(name)

            # I assume the last paren_item is the role shorthand
            paren_items = self.RE_PAREN_ITEM.findall(item)
            short_hand = paren_items[-1]

            if short_hand in short_hands:
                print(f'Duplikeret rolle forkortelse: {short_hand}')

            short_hands.append(short_hand)

    def check_band(self, is_sang=False):
        if is_sang and not self.RE_BAND.search(self.content):
            print("[SANG] Manglende bandkommentar")

    def check_lydeffekter(self):
        matches = self.RE_LYDEFFEKTER.findall(self.content)
        # Placeholder
        return matches

    def check_rekvisitter(self):
        matches = self.RE_REKVISITTER.findall(self.content)
        for env, val in matches:
            if "(R)" not in val and "(P)" not in val:
                print(f"[REKVISIT] Rekvisit uden R/P markering: {val.strip()}")


    def check_scene_commands(self):

        last_command, last_index = "", -1

        for i in range(len(self.lines)):
            line = self.lines[i].strip()
            if self.RE_SCENE.match(line):

                if self.RE_FULDSCENE.match(line) and self.RE_CURLY_EMPTY.search(line):
                    print(f"[SCENE] Tom \\fuldscene{{}}. Overvej om der skal stå noget på scenen, og skriv det i krølleparenteserne. Linje {i+1}")

                if self.RE_FULDSCENE.match(line) and self.RE_FULDSCENE.match(last_command):
                    print(f'[SCENE] Fuldscene -> fuldscene overgang fra linje {last_index+1} til linje {i+1}')

                if not self.RE_PERFECT_SCENE.fullmatch(line):
                    print(f"[SCENE] Scenekommando skal slutte med {{}}\\\\ på linje {i+1}")

                prev, next = self.lines[i-1], self.lines[i+1]
                if not (prev == "\n" and next == "\n") :
                    print(f"[SCENE] Der skal være blanke linjer over og under \\forscene{{}} eller \\fuldscene{{}} på linje {i+1}")

                last_command, last_index = line, i

        # Alt skal slutte på forscenen
        if not self.RE_FORSCENE.match(last_command):
            print(f"[SCENE] Slutter ikke på forscenen")

def main():
    parser = argparse.ArgumentParser(description="Validate .tex file")
    parser.add_argument("files", nargs="+", help="Filenames to check")
    args = parser.parse_args()

    for f in args.files:
        print(f"--- checker {f} ---")
        validator = RevyParser(f)
        validator.validate()


if __name__ == "__main__":
    main()
