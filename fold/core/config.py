from __future__ import annotations
from types import NoneType
from typing import TYPE_CHECKING, Iterable, Optional, Dict, List, Set
from pathlib import Path

from pydantic import BaseModel, validator
from pydantic.fields import ModelField

from fold.utils.plugin import PluginManager

if TYPE_CHECKING:
    from fold.plugins.config import ConfigFilePlugin

Content = str | int | float | bool | NoneType | List["Content"] | Dict[str, "Content"]


class ConfigError(Exception):
    pass


class ConfigManager:
    def __init__(self, config: BaseModel, *args, **kwargs) -> None:
        self.config = config
        
    @classmethod
    def parseConfig(cls, config: Content) -> BaseModel | List[BaseModel]:
        match config:
            case str():
                return cls.parseStr(config)
            case int():
                return cls.parseInt(config)
            case float():
                return cls.parseFloat(config)
            case bool():
                return cls.parseBool(config)
            case NoneType():
                return cls.parseNone(config)
            case list():
                return cls.parseList(config)
            case dict():
                return cls.parseDict(config)

    @classmethod
    def parseStr(cls, config: str) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def parseInt(cls, config: int) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def parseFloat(cls, config: float) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def parseBool(cls, config: bool) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def parseNone(cls, config: NoneType) -> BaseModel:
        raise NotImplementedError

    @classmethod
    def parseList(cls, config: List[Content]) -> List[BaseModel]:
        return [cls.parseConfig(conf) for conf in config]

    @classmethod
    def parseDict(cls, config: Dict[str, Content]) -> BaseModel:
        raise NotImplementedError


class BaseConfig(BaseModel):
    class Config:
        validate_all = True
        arbitrary_types_allowed = True
        
    @validator("*", pre=True, always=True)
    def name(cls, content: Content, field: ModelField):
        manager: ConfigManager = field.type_
        config = manager.parseConfig(content)
        return manager(config)
    
    @classmethod
    @property
    def DEFAULT_PARSERS(cls) -> Set[ConfigFilePlugin]:
        return PluginManager(ConfigFilePlugin).discover("fold.plugins.config")

    @classmethod
    def fromText(
        cls, text: str, parsers: Optional[Iterable[ConfigFilePlugin]] = None
    ) -> BaseConfig:
        """Parse a config as a single string

        Args:
            text (str): config
            parsers (Iterable[ConfigFile], None): File parsers to use, default to fold.config

        Raises:
            ConfigError: None of the parsers worked

        Returns:
            BaseConfig: Base config model
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
        return BaseConfig(**config)

    @classmethod
    def fromPath(
        cls, path: Path, parsers: Optional[Iterable[ConfigFilePlugin]] = None
    ) -> BaseConfig:
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
