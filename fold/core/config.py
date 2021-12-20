from __future__ import annotations

from typing import Any, Iterable
import abc


class ConfigParser(abc.ABC):
    @classmethod
    def fromText(cls, text: str) -> dict:
        pass


class ConfigSection(abc.ABC):
    NAME: str = None

    def __init__(self, content: Any) -> None:
        pass

    def parse(self) -> Any:
        pass


class Config:
    def __init__(self, conf: dict, sectionParsers: Iterable[ConfigSection]) -> None:
        # Create the mapping between section keys and their parsers
        sectionParserMap = {
            sectionParser.NAME: sectionParser for sectionParser in sectionParsers
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
        configParser: ConfigParser,
        sectionParsers: Iterable[ConfigSection],
    ) -> Config:
        conf: dict = configParser.fromText(conf)
        return cls(conf, sectionParsers)
