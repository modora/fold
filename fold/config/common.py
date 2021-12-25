from typing import Any, Iterable, Optional, Dict
from abc import ABC, abstractmethod
from pathlib import Path

from fold import Plugin, PluginManager

Content = Dict[str, Any]


class ConfigError(Exception):
    pass


class ConfigFileParser(ABC, Plugin):
    EXTENSIONS: Iterable[str] = set()

    @classmethod
    @abstractmethod
    def fromText(cls, text: str) -> Content:
        pass


class ConfigSectionParser(ABC, Plugin):
    def __init__(self, content: Content, manager: PluginManager) -> None:
        self.content = content
        self.manager = manager

    @abstractmethod
    def parse(self, *args, **kwargs) -> Any:
        pass


class ConfigManager(Plugin):
    def __init__(
        self,
        sections: Iterable[ConfigSectionParser],
        parsers: Optional[Iterable[ConfigFileParser]] = None,
    ) -> None:
        self.sections = {section.name: section for section in sections}
        self.parsers = parsers or set()

    def _parseContent(self, content: Content) -> Content:
        parsedContent: Content = {}
        for sectionName, sectionContent in content.items():
            parsedContent[sectionName] = self.sections[sectionName](
                sectionContent
            ).parse()
        return parsedContent

    def fromText(self, text: str, parser: Optional[ConfigFileParser] = None) -> Content:
        if parser:
            content = parser.fromText(text)

            return self._parseContent(content)

        # The parser is not defined, brute force the parsers.
        for parser in self.parsers:
            try:
                return self.fromText(text, parser)
            except Exception:
                pass
        raise ConfigError(f"Unable to parse {text}")

    def fromPath(self, path: str | Path, parser: Optional[ConfigFileParser] = None):
        path = Path(path).resolve()  # convert to Path

        # Get the contents of the file and pass to the parser
        with open(path, "r", encoding="UTF-8") as file:
            text = file.read()
        if parser:
            return self.fromText(text, parser)

        # If the parser is not defined, then discover the parser first. Discovery is attempted using the file extension.
        # If that doesn't work, brute force the remaining parsers.
        parsers = set(self.parsers)

        # Try discovering the parser based off the file extension
        ext = path.suffix
        for parser in parsers:
            if ext.lower() in [ext.lower() for ext in parser.EXTENSIONS]:
                try:
                    return self.fromText(text, parser)
                except Exception:
                    pass
            parsers.remove(parser)

        # Brute force all remaining parsers
        for parser in parsers:
            try:
                return self.fromText(text, parser)
            except Exception:
                pass

        raise ConfigError(f"Unable to parse {path}")
