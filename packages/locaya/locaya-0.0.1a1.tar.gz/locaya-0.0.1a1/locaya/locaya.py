from locaya.language import Language
from locaya.loader.base import BaseLoader
from locaya.localization import Localization


class Locaya:
    def __init__(self, loader: BaseLoader, *, strict: bool = False):
        self._loader: BaseLoader = loader
        self._strict: bool = strict
        self._localizations: dict[str, Localization] | None = None

    def load(self):
        """
        Load localizations by loader
        """
        self._localizations = self._loader()

    def get(self, code: str) -> Localization:
        """
        Returns localization with specified code
        If ``Locaya`` is in `strict mode`, raises exception if localization is not exists,
        else returns empty localization
        :param code: localization code
        :return: instance of ``Localization``
        """
        if self._strict:
            return self._localizations[code]
        return self._localizations.get(code) or Localization(Language(code), {})


