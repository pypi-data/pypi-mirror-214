import glob
import os.path

from locaya import localization


class Locaya:
    def __init__(self, localizations: dict[str, localization.Localization] = None, strict: bool = False):
        self.localizations = localizations if localizations else {}
        self.strict = strict

    def add(self, _localization: localization.Localization):
        self.localizations[_localization.meta.code] = _localization

    def load(self, text: str):
        self.add(localization.load(text, self.strict))

    def load_file(self, path: str):
        with open(path) as file:
            self.load(file.read())

    def load_directory(self, path: str):
        files = glob.glob(os.path.join(path, "*.yml"))
        for file in files:
            self.load_file(file)

    def get(self, code: str) -> localization.Localization:
        return self.localizations.get(code)

    def __contains__(self, item: str) -> bool:
        return item in self.localizations

