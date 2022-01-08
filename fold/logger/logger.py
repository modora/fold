from typing import (
    TYPE_CHECKING,
    Any,
    List,
    TypedDict,
    Optional,
    IO,
    Callable,
    Coroutine,
)
from logging import Handler
from pathlib import Path
from functools import partial
import sys

from functional import seq
from loguru import logger

from fold.core import Manager
from fold.utils import loadObjectDynamically

if TYPE_CHECKING:
    from fold.config import Config

class RawLogHandlerConfig(TypedDict):
    level: Optional[int | str]
    format: Optional[str]
    filter: Optional[str | dict]
    colorize: Optional[bool]
    serialize: Optional[bool]
    backtrace: Optional[bool]
    diagnose: Optional[bool]
    enqueue: Optional[bool]
    catch: Optional[bool]
    kwargs: Optional[dict]
    # Custom objects will be dynamically loaded and override the key-value pair
    custom_sink: Optional[str]  # required if sink == "custom"
    custom_format: Optional[str]  # required if format == "custom"
    custom_filter: Optional[str]  # required if filter == "custom"

RawLogConfig = List[RawLogHandlerConfig]

ParsedSink = str | IO | Path | Callable | Coroutine | Handler
ParsedFormat = Optional[str | Callable]
ParsedFilter = Optional[str | dict | Callable]


class ParsedLogHandlerConfig(TypedDict):
    sink: ParsedSink
    level: Optional[int | str]
    format: ParsedFormat
    filter: ParsedFilter
    colorize: Optional[bool]
    serialize: Optional[bool]
    backtrace: Optional[bool]
    diagnose: Optional[bool]
    enqueue: Optional[bool]
    catch: Optional[bool]
    kwargs: Optional[dict]

ParsedLogConfig = List[ParsedLogHandlerConfig]

class LogHandler:
    @classmethod
    def checkConfig(cls, config: RawLogHandlerConfig):
        """Checks whether the specified input config is valid

        If the config is valid, nothing will happen; otherwise an exception is raised.

        Args:
            config (RawLogHandlerConfig): Configuration to check
        Raises:
            KeyError: Unknown key
        """

        seq(config.items()).map(
            partial(cls._checkInvalidKey, reference=RawLogHandlerConfig)
        ).map(partial(cls._checkConfigTypes, reference=RawLogHandlerConfig))

    # Config check methods
    @staticmethod
    def _checkInvalidKey(key: str, value: Any, reference: Any):
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
    def _checkConfigTypes(key: str, value: Any, reference: Any):
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
        cls, config: RawLogHandlerConfig, validate: Optional[bool] = True
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
        cls, config: RawLogHandlerConfig, validate: Optional[bool] = True
    ) -> ParsedSink:
        sink = config["sink"]
        match sink:
            case "stdout":
                return sys.stdout
            case "stderr":
                return sys.stderr
            case "custom":
                # Attempt to load the object
                # obj = loadObjectDynamically(sink)
                obj=None
                # Validate whether the object is a valid sink
                if validate:
                    cls._checkConfigTypes("sink", obj, reference=ParsedLogHandlerConfig)

                return obj  # override the sink str
            # The stdin case exists for safety reasons. IDK what happens when you pipe to stdin but I imagine it's bad.
            # Therefore, just assume stdin is a filename
            case _:  # Treat the sink as a path
                return Path(sink)

    @classmethod
    def _parseFormatConfig(
        cls, config: RawLogHandlerConfig, validate: Optional[bool] = True
    ) -> ParsedFormat:
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
        cls, config: RawLogHandlerConfig, validate: Optional[bool] = True
    ) -> ParsedFilter:
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

class LogManager(Manager):
    NAME = "log"
    
    def __init__(self, config: Config) -> None:
        logConfig = config["log"]
        for handlerConfig in logConfig:
            logger.add(**handlerConfig)
    
    @classmethod
    def parseConfig(cls, config: RawLogConfig) -> ParsedLogConfig:
        return [LogHandler.parseConfig(handerConfig) for handerConfig in config]
