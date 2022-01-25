from typing import Dict, Iterable
from abc import abstractmethod

from fold.core import Plugin, Content


class ConfigFilePlugin(Plugin):
    EXTENSIONS: Iterable[str] = set()

    @classmethod
    @abstractmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        pass
