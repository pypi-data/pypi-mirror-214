from abc import ABC, abstractmethod

from locaya.localization import Localization


class BaseLoader(ABC):
    @abstractmethod
    def __call__(self) -> dict[str, Localization]:
        raise NotImplementedError
