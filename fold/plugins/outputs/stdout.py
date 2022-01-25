from __future__ import annotations
from typing import TYPE_CHECKING, Any
import sys

from .common import OutputPlugin, OutputPluginConfig

if TYPE_CHECKING:
    from fold.core import Content


class StdoutConfig(OutputPluginConfig):
    # It's stdout... there is no addtional configuration.
    class Config:
        extra = "forbid"


class Stdout(OutputPlugin):
    def __init__(self, config: StdoutConfig, *args, **kwargs) -> None:
        super().__init__(config, *args, **kwargs)

    @classmethod
    def parseConfig(cls, config: Content, *args, **kwargs) -> StdoutConfig:
        return super().parseConfig(config, *args, **kwargs)

    def write(self, data: Any):
        if data is None:
            data = ""
        sys.stdout.write(str(data) + "\n")
