import re
import string
import unicodedata

class Klean:

    def __init__(self, text):
        self.text = text

    def upper(self):
        self.text = self.text.upper()
        return self

    def lower (self):
        self.text = self.text.lower()
        return self

    def strip_html(self) -> str:
        """remove html tags from string"""
        self.text = re.sub(r"<[^<]+?>", "", self.text)
        return self

    def unslugify(self) -> str:
        l = re.sub(r"-|_", " ", self.text)
        return self

    def slugify(self) -> str:
        if isinstance(self.text, str):
            stringvar = stringvar.decode("utf-8")
        slug = unicodedata.normalize("NFKD", self.text)
        slug = slug.encode("ascii", "ignore")
        slug = slug.strip().lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        l = re.sub(r" ", "-", slug)
        self.text = l
        return self


    def chop(self, step) -> list[str]:
        l = []
        i = 0
        while i <= len(self.text):
            l.append(self.text[i : i + step])
            i = i + step
        return l

    def surround(self, prefix: str, suffix: str):
        self.text = "".join([prefix, self.text, suffix])
        return self

    def clean(self) -> str:
        """squeeze multiple spaces and trim"""
        s = re.sub(r"\s+", " ", self.text)
        self.text = s.strip()
        return self


    def kebab(self) -> str:
        """hello world --> hello-world"""
        s = self.text.lower().split()
        self.text = "-".join(s)
        return self

    def pascal(self) -> str:
        """hello world --> HelloWorld"""
        s = [word.title() for word in self.text.split()]
        self.text = "".join(s)
        return self


    def camel(self) -> str:
        """hello world --> helloWorld"""
        s = self.text.split()
        s1 = [word.title() for word in s[1:]]
        s2 = [s[0].lower()] + s1
        self.text = "".join(s2)
        return self

    def snake(self) -> str:
        """hello world --> hello_world"""
        s = self.text.lower().split()
        self.text = "_".join(s)
        return self

    def capital(self):
        self.text = self.text.title()
        return self

    def append(self, stringvar:str):
        self.text = self.text + stringvar
        return self

    def prepend(self, stringvar:str):
        self.text = stringvar + self.text
        return self

    def remove_punct(self):
        self.text = self.text.translate(str.maketrans("", "", string.punctuation))
        return self

    def trim(self):
        self.text = self.text.trim()
        return self

    def to_text(self):
        return self.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text
