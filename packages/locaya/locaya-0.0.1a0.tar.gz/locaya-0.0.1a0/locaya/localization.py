import logging
import re
from typing import Final

import yaml

_META_LINE_PATTERN: Final[re.Pattern] = re.compile(r"^#.+\$(.+)$", re.RegexFlag.MULTILINE)
_VARIABLE_PATTERN: Final[re.Pattern] = re.compile(r"\$(\S+)")
_CODE_OP: Final[str] = "code"
_NAME_OP: Final[str] = "name"
_AUTHOR_OP: Final[str] = "author"
_DESCRIPTION_OP: Final[str] = "description"

_logger = logging.getLogger(__name__)


class LocalizationMeta:
    def __init__(
            self,
            variables: dict[str, str],
            code: str,
            name: str | None,
            author: str | None,
            description: str | None
    ):
        self.variables = variables
        self.code = code
        self.name = name
        self.author = author
        self.description = description

    @classmethod
    def parse(cls, lines: list[str]):
        lines = [line.strip() for line in lines]
        meta_dict = {}
        for line in lines:
            op, arg = line.split(" ", 1)
            meta_dict[op] = arg
        code = meta_dict.pop(_CODE_OP)
        name = meta_dict.pop(_NAME_OP, None)
        author = meta_dict.pop(_AUTHOR_OP, None)
        description = meta_dict.pop(_DESCRIPTION_OP, None)
        return cls(meta_dict, code, name, author, description)


class Localization:
    def __init__(self, meta: LocalizationMeta, strings: dict[str, str], strict: bool):
        self.meta = meta
        self.strings = strings
        self.strict = strict

    def __call__(self, key: str, **kwargs) -> str:
        try:
            return self.strings[key].format(**kwargs)
        except KeyError as error:
            _logger.exception("Localization error: code=%s key=%s", self.meta.code, key, exc_info=error)
            if self.strict:
                raise
            return key


def _render_variables(line: str, variables: dict[str, str], pattern: re.Pattern):
    for match in re.finditer(pattern, line):
        line = line.replace(match.group(0), variables.get(match.group(1), match.group(1)))
    return line


def load(raw_yaml: str, strict: bool) -> Localization:
    meta = LocalizationMeta.parse(re.findall(_META_LINE_PATTERN, raw_yaml))
    strings = {
        key: _render_variables(value, meta.variables, _VARIABLE_PATTERN)
        for key, value in yaml.safe_load(raw_yaml).items()
    }
    return Localization(meta, strings, strict)
