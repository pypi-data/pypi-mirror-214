from locaya.language import Language


class Localization:
    def __init__(self, language: Language, dictionary: dict[str, str]):
        self._language = language
        self._dictionary = dictionary

    @property
    def language(self) -> Language:
        return self._language

    def __call__(self, key: str, *args, **kwargs) -> str:
        """
        Returns localized string for ``key``, supports formatting by args and kwargs.
        If string not exist, returns ``key``
        :param key: string key
        :param args: formatting args
        :param kwargs: formatting kwargs
        :return: localized string
        """
        return self._dictionary.get(key) or key
