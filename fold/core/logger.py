from typing import (
    Any as _Any,
    List as _List,
    TypedDict as _TypedDict,
    Optional as _Optional,
    IO as _IO,
    Callable as _Callable,
    Coroutine as _Coroutine,
)
from logging import Handler as _Handler
from loguru import logger
from pathlib import Path as _Path
from functional import seq as _seq
from functools import partial as _partial
import sys as _sys

from .config import ConfigSectionParser as _ConfigSectionParser
from fold.utils import loadObjectDynamically


class RawLogHandlerConfig(_TypedDict):
    sink: str
    level: _Optional[int | str]
    format: _Optional[str]
    filter: _Optional[str | dict]
    colorize: _Optional[bool]
    serialize: _Optional[bool]
    backtrace: _Optional[bool]
    diagnose: _Optional[bool]
    enqueue: _Optional[bool]
    catch: _Optional[bool]
    kwargs: _Optional[dict]
    # Custom objects will be dynamically loaded and override the key-value pair
    custom_sink: _Optional[str]  # required if sink == "custom"
    custom_format: _Optional[str]  # required if format == "custom"
    custom_filter: _Optional[str]  # required if filter == "custom"


_ParsedSink = str | _IO | _Path | _Callable | _Coroutine | _Handler
_ParsedFormat = _Optional[str | _Callable]
_ParsedFilter = _Optional[str | dict | _Callable]


class ParsedLogHandlerConfig(_TypedDict):
    sink: _ParsedSink
    level: _Optional[int | str]
    format: _ParsedFormat
    filter: _ParsedFilter
    colorize: _Optional[bool]
    serialize: _Optional[bool]
    backtrace: _Optional[bool]
    diagnose: _Optional[bool]
    enqueue: _Optional[bool]
    catch: _Optional[bool]
    kwargs: _Optional[dict]


class _LogHandler:
    @classmethod
    def checkConfig(cls, config: RawLogHandlerConfig):
        """Checks whether the specified input config is valid

        If the config is valid, nothing will happen; otherwise an exception is raised.

        Args:
            config (RawLogHandlerConfig): Configuration to check
        Raises:
            KeyError: Unknown key
        """

        _seq(config.items()).map(
            _partial(cls._checkInvalidKey, reference=RawLogHandlerConfig)
        ).map(_partial(cls._checkConfigTypes, reference=RawLogHandlerConfig))

    # Config check methods
    @staticmethod
    def _checkInvalidKey(key: str, value: _Any, reference: _Any):
        """Check whether a key is known

        Args:
            key (str): Config key
            value (Any): Config value
            reference(Any): Reference object for validity check

        Raises:
            KeyError: Key is unknown
        """
        if key not in dir(reference):
            raise KeyError(f"Unknown key: {key}")

    @staticmethod
    def _checkConfigTypes(key: str, value: _Any, reference: _Any):
        """Check whether config value is the expected type

        Args:
            key (str): Config key
            value (Any): Config value
            reference (Any): Reference object for validity check

        Raises:
            TypeError: Value type is unknown
        """
        expectedType = getattr(reference, key)
        if not isinstance(value, expectedType):
            raise TypeError(f"Expected {key} to be a {expectedType}")

    @classmethod
    def parseConfig(
        cls, config: RawLogHandlerConfig, validate: _Optional[bool] = True
    ) -> ParsedLogHandlerConfig:
        if validate:
            cls.checkConfig(config)  # Check whether config is valid
        parsedConfig = ParsedLogHandlerConfig(config.copy())

        # Remove the custom_* keys
        for key in parsedConfig.keys():
            if key.startswith("custom_"):
                del parsedConfig[key]

        # Sink handling
        parsedConfig["sink"] = cls._parseSinkConfig(config, validate=validate)

        # Format handling
        if result := cls._parseFormatConfig(config, validate=validate):
            parsedConfig["format"] = result

        # Filter handling
        if result := cls._parseFilterConfig(config, validate=validate):
            parsedConfig["filter"] = result

        return parsedConfig

    @classmethod
    def _parseSinkConfig(
        cls, config: RawLogHandlerConfig, validate: _Optional[bool] = True
    ) -> _ParsedSink:
        sink = config["sink"]
        match sink:
            case "stdout":
                return _sys.stdout
            case "stderr":
                return _sys.stderr
            case "custom":
                # Attempt to load the object
                obj = loadObjectDynamically(sink)
                # Validate whether the object is a valid sink
                if validate:
                    cls._checkConfigTypes("sink", obj, reference=ParsedLogHandlerConfig)

                return obj  # override the sink str
            # The stdin case exists for safety reasons. IDK what happens when you pipe to stdin but I imagine it's bad.
            # Therefore, just assume stdin is a filename
            # TODO: Apparently _ is not a catch all. so what is?
            case [_, "stdin"]:  # Treat the sink as a path
                return _Path(sink)

    @classmethod
    def _parseFormatConfig(
        cls, config: RawLogHandlerConfig, validate: _Optional[bool] = True
    ) -> _ParsedFormat:
        format = config.get("format")
        match format:
            case "custom":
                # Attempt to load the object
                obj = loadObjectDynamically(format)
                # Validate whether the object is a valid format
                if validate:
                    cls._checkConfigTypes(
                        "format", obj, reference=ParsedLogHandlerConfig
                    )

                return obj  # override the format str
            # Either no formatter is defined or it's (assumed to be) a loguru built-in formatter so no need to handle
            # anything
            case _:
                return format

    @classmethod
    def _parseFilterConfig(
        cls, config: RawLogHandlerConfig, validate: _Optional[bool] = True
    ) -> _ParsedFilter:
        filter = config.get("filter")
        match filter:
            case "custom":
                # Attempt to load the object
                obj = loadObjectDynamically(filter)
                # Validate whether the object is a valid format
                if validate:
                    cls._checkConfigTypes(
                        "format", obj, reference=ParsedLogHandlerConfig
                    )

                return obj  # override the filter str
            # Either no formatter is defined or it's (assumed to be) a loguru built-in formatter so no need to handle
            # anything
            case _:
                return filter


class LogConfigSectionParser(_ConfigSectionParser):
    NAME = "log"

    def __init__(self, content: _List[RawLogHandlerConfig]) -> None:
        super().__init__(content)

    def parse(self) -> _List[ParsedLogHandlerConfig]:
        return [_LogHandler.parseConfig(handler) for handler in self.content]


def configureLogger(config: _List[ParsedLogHandlerConfig]):
    for handler in config:
        logger.add(**handler)
