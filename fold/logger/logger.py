from __future__ import annotations
import sys
from typing import (
    TYPE_CHECKING,
    List,
    Optional,
    Callable,
    Coroutine,
)
from logging import Handler
from pathlib import Path

from pydantic import BaseModel, root_validator, validator, Field
from loguru import logger

from fold.plugin import Plugin
from fold.utils import loadObjectDynamically

if TYPE_CHECKING:
    from fold.config import Content

class LogHandlerConfig(BaseModel):
    sink: str | Path | Callable | Coroutine | Handler | object
    level: Optional[int | str]
    format: Optional[str | Callable]
    filter: Optional[str | dict | Callable]
    colorize: Optional[bool]
    serialize: Optional[bool]
    backtrace: Optional[bool]
    diagnose: Optional[bool]
    enqueue: Optional[bool]
    catch: Optional[bool]
    # Custom objects will be dynamically loaded and override the key-value pair
    custom_sink: Optional[str] = Field(
        default=None,
        exclude=True,
    )  # required if sink == "custom"
    custom_format: Optional[str] = Field(
        default=None, exclude=True
    )  # required if format == "custom"
    custom_filter: Optional[str] = Field(
        default=None, exclude=True
    )  # required if filter == "custom"

    class Config:
        arbitrary_types_allowed = True
        extra = 'allow'

    @root_validator(pre=True)
    def import_custom_fields(cls, values):
        """Replace custom fields with the import path specified"""
        CUSTOM_FIELDS = ["sink", "format", "filter"]
        for field in CUSTOM_FIELDS:
            if value := values.get(field):
                if value == "custom":
                    name = values[f"custom_{field}"]
                    values[field] = loadObjectDynamically(name)
        return values
    
    @validator('sink', pre=True)
    def special_sink(cls, value):
        match value:
            case "stdout":
                return sys.stdout
            case "stderr":
                return sys.stderr
            case _:
                return value
            
    @validator("sink")
    def filelike_sink(cls, value):
        # if generic object, test whether it contains a write method
        if not isinstance(value, str | Path | Callable | Coroutine | Handler):
            if hasattr(value, "write") and callable(value.write):
                return value
            raise TypeError("Object does not have a write method defined")
        return value
            
            
    @validator("sink")
    def str_sink(cls, value):
        # Recast str as Path
        if isinstance(value, str):
            return Path(value)
        return value


class LogManager(Plugin):
    def __init__(self, config: List[LogHandlerConfig], *args, **kwargs) -> None:
        logger.remove()  # clear any existing handlers
        for handlerConfig in config:
            logger.add(**handlerConfig.dict(exclude_none=True, exclude_unset=True))

    @classmethod
    def parseConfig(cls, config: Content, *args, **kwargs) -> List[LogHandlerConfig]:
        return [LogHandlerConfig(**conf) for conf in config]
