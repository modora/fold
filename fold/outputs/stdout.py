from typing import Any
import sys

from .common import OutputPlugin, OutputHandlerConfig


class StdoutHandlerConfig(OutputHandlerConfig):
    # It's stdout... there is no configuration.
    pass


class StdoutOutputPlugin(OutputPlugin):
    NAME = "stdout"

    @classmethod
    def parseConfig(cls, config: StdoutHandlerConfig) -> StdoutHandlerConfig:
        parsedConfig = config.copy()
        return parsedConfig

    def write(self, data: Any):
        if data is None:
            data = ""
        sys.stdout.write(str(data) + "\n")
