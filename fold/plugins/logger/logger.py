from __future__ import annotations
import sys
from typing import (
    Iterable,
    Optional,
    Callable,
    Coroutine,
    Dict
)
from logging import Handler
from pathlib import Path

from pydantic import BaseModel, root_validator, validator, Field
from loguru import logger

from fold.core import ConfigManager, Content
from fold.utils.imp import importFromString

class LogHandlerConfig(BaseModel):
    sink: str | Path | Callable | Coroutine | Handler
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
                    values[field] = importFromString(name)
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
        # if not a expected sink, test whether it contains a write method
        if not any(isinstance(value, cls.__fields__["sink"])):
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


class LogManager(ConfigManager):
    def __init__(self, config: LogHandlerConfig | Iterable[LogHandlerConfig], *args, **kwargs):
        if isinstance(config, LogHandlerConfig):
            config = [config]
        
        super().__init__(config)
        
        self.remove()  # clear any existing handlers
        self.configure(config)
    
    @classmethod
    def parseDict(cls, config: Dict[str, Content], *args, **kwargs) -> LogHandlerConfig:
        return LogHandlerConfig(**config)
        
    def remove(self, *args, **kwargs):
        logger.remove(*args, **kwargs)
        
    def add(self, *args, **kwargs):
        logger.add(*args, **kwargs)
        
    def configure(self, config: Iterable[LogHandlerConfig]):
        for conf in config:
            self.add(**conf.dict(exclude_none=True, exclude_unset=True))
