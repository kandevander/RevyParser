import os
import re
import argparse


class RevyParser:
    RE_SCENE_START = re.compile(r'(\\fuldscene|\\forscene)', re.DOTALL)
    RE_SCENE_END = re.compile(r'\\forscene{}\\')
    RE_TID = re.compile(r'\\tid{(\d{1,2}:\d{2})}')
    RE_ITEM = re.compile(r'\\item\s.+\s\(.+\)\s(?:\\sketchrolle|\\sangrolle)', re.DOTALL)
    RE_BAND = re.compile(r'\\begin{Bandkommentar}(.*?)\\end{Bandkommentar}', re.DOTALL)
    RE_LYDEFFEKTER = re.compile(r'\\lyd{(.+?)}')
    RE_REKVISITTER = re.compile(r'\\begin{(Rekvisitter)}(.*?)\\end{\1}', re.DOTALL)
    RE_HASHTAG = re.compile(r'#')
    RE_COLON = re.compile(r':')
    RE_GAASEOEJNE = re.compile(r'[“”]')

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

    def check_title(self):
        for line in self.lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("%"):
                title = stripped
                if self.RE_HASHTAG.search(title):
                    print(f"[TITEL] Titel indeholder #: {title}")
                if self.RE_COLON.search(title):
                    print(f"[TITEL] Titel indeholder kolon: {title}")
                if title == "Navn":
                    print(f"[TITEL] Titel er ugyldig: {title}")
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
        roles = []
        for item in self.RE_ITEM.findall(self.content):
            name = item.strip()
            lname = name.lower()

            if lname in roles:
                print(f"[ROLLE] Duplikatrolle: {name}")
            roles.append(lname)

            if "," in name:
                print(f"[ROLLE] Komma i rollenavn: {name}")

            if "{" in name:
                print(
                    "[ROLLE] Krølleparenteser efter \\sketchrolle eller \\sangrolle: "
                    f"{name}"
                )

        if not roles:
            print("[ROLLE] Ingen roller fundet")

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
        for i, line in enumerate(self.lines, start=-1):
            if self.RE_SCENE_START.search(line):
                print(line)
            if self.RE_SCENE_END.search(line):
                pass  # Slutter korrekt

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
