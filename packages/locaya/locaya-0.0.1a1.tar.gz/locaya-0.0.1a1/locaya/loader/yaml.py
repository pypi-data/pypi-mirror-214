import os
from typing import Final

import yaml

from locaya.language import Language
from locaya.loader.base import BaseLoader
from locaya.localization import Localization


_CODE_KEY: Final[str] = "$code"
_NAME_KEY: Final[str] = "$name"
_AUTHOR_KEY: Final[str] = "$author"
_DESCRIPTION_KEY: Final[str] = "$description"


class YamlLoader(BaseLoader):
    """
    Loads localizations from directory with YAML files
    """
    def __init__(self, directory: str):
        """
        :param directory: path to directory with localization YAML files
        """
        self._directory: str = directory

    def __call__(self) -> dict[str, Localization]:
        result: dict[str, Localization] = {}
        for file_path in [f for f in os.listdir(self._directory) if os.path.isfile(os.path.join(self._directory, f))]:
            with open(os.path.join(self._directory, file_path)) as file:
                raw_dict = yaml.safe_load(file)
            code = raw_dict[_CODE_KEY]
            result[code] = Localization(
                Language(
                    raw_dict.pop(_CODE_KEY),
                    raw_dict.pop(_NAME_KEY, None),
                    raw_dict.pop(_AUTHOR_KEY, None),
                    raw_dict.pop(_DESCRIPTION_KEY, None)
                ),
                raw_dict
            )
        return result
