from __future__ import annotations
from typing import Iterable, Optional, Dict, List, Set
from abc import abstractmethod
from pathlib import Path

from fold.core import Plugin, PluginManager

Content = str | int | float | bool | List["Content"] | Dict[str, "Content"]


class ConfigError(Exception):
    pass


class ConfigFilePlugin(Plugin):
    EXTENSIONS: Iterable[str] = set()

    @classmethod
    @abstractmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        pass


class Config:
    @classmethod
    @property
    def DEFAULT_PARSERS(cls) -> Set[ConfigFilePlugin]:
        return PluginManager(ConfigFilePlugin).discover("fold.config")

    def __init__(self, config: Dict[str, Content]) -> None:
        pass

    @classmethod
    def fromText(
        cls, text: str, parsers: Optional[Iterable[ConfigFilePlugin]] = None
    ) -> Config:
        """Parse a config as a single string

        Args:
            text (str): config
            parsers (Iterable[ConfigFile], None): File parsers to use, default to fold.config

        Raises:
            ConfigError: None of the parsers worked

        Returns:
            Config: [description]
        """
        # If the parsers are not defined, then discover the parsers first.
        if parsers is None:
            parsers = cls.DEFAULT_PARSERS

        # Brute force all parsers defined
        for parser in parsers:
            try:
                config = parser.fromText(text)
                break
            except Exception:
                pass
        else:
            # None of them worked...
            raise ConfigError(f"Failed to parse {text}")
        return Config(config)

    @classmethod
    def fromPath(
        cls, path: Path, parsers: Optional[Iterable[ConfigFilePlugin]] = None
    ) -> Config:
        # If the parsers are not defined, then discover the parsers first.
        if parsers is None:
            parsers = cls.DEFAULT_PARSERS

        with open(path, "r", encoding="UTF-8") as file:
            text = file.read()

        # Try to parse based off the file extension
        ext = path.suffix.lower()
        extParsers = {
            parser
            for parser in parsers
            if ext in {ext.lower() for ext in parser.EXTENSIONS}
        }
        try:
            return cls.fromText(text, extParsers)
        except ConfigError:  # ext parsers failed
            parsers = parsers - extParsers

        # Just brute force the remaining parsers
        try:
            return cls.fromText(text, parsers)
        except ConfigError as e:
            raise ConfigError(f"Failed to parse {path}") from e
