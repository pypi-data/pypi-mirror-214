class Language:
    def __init__(self, code: str, name: str = None, author: str = None, description: str = None):
        self._code = code
        self._name = name
        self._author = author
        self._description = description

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def author(self) -> str | None:
        return self._author

    @property
    def description(self) -> str | None:
        return self._description

    def __eq__(self, other) -> bool:
        if not isinstance(other, Language):
            return False
        return (
                self.code == other.code
                and self.name == other.name
                and self.author == other.author
                and self.description == other.description
        )
