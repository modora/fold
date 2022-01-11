from __future__ import annotations
from typing import TYPE_CHECKING, Any
import sys

from .common import OutputPlugin, OutputHandlerConfig

if TYPE_CHECKING:
    from fold.config import Content


class StdoutConfig(OutputHandlerConfig):
    # It's stdout... there is no addtional configuration.
    class Config:
        extra = "forbid"


class Stdout(OutputPlugin):
    def __init__(self, config: StdoutConfig, *args, **kwargs) -> None:
        super().__init__(config, *args, **kwargs)

    @classmethod
    def parseConfig(cls, config: Content) -> StdoutConfig:
        return StdoutConfig(**config)

    def write(self, data: Any):
        if data is None:
            data = ""
        sys.stdout.write(str(data) + "\n")
