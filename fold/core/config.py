from __future__ import annotations

from typing import Any, Iterable, Dict
from abc import ABC, abstractmethod

from .plugin import Plugin


class ConfigFileParser(ABC, Plugin):
    @classmethod
    @abstractmethod
    def fromText(cls, text: str) -> dict:
        pass


class ConfigSectionParser(ABC, Plugin):
    NAME: str = None

    def __init__(self, content: Any) -> None:
        self.content = content

    @abstractmethod
    def parse(self) -> Any:
        pass


class Config:
    def __init__(
        self, conf: dict, sectionParsers: Iterable[ConfigSectionParser]
    ) -> None:
        # Create the mapping between section keys and their parsers
        sectionParserMap = {
            sectionParser.name: sectionParser for sectionParser in sectionParsers
        }

        # Parse the actual config now
        self._conf = {}
        for section, content in conf.items():
            sectionParser = sectionParserMap[section]
            parsedSection = {section: sectionParser(content).parse()}
            self._conf.update(parsedSection)

    @classmethod
    def fromText(
        cls,
        conf: str,
        configParser: ConfigFileParser,
        sectionParsers: Iterable[ConfigSectionParser],
    ) -> Config:
        conf: dict = configParser.fromText(conf)
        return cls(conf, sectionParsers)
