from typing import Any
import sys

from .common import OutputPlugin, OutputHandlerConfig


class StdoutConfig(OutputHandlerConfig):
    # It's stdout... there is no configuration.
    pass


class Stdout(OutputPlugin):
    @classmethod
    def parseConfig(cls, config: StdoutConfig) -> StdoutConfig:
        parsedConfig = config.copy()
        return parsedConfig

    def write(self, data: Any):
        if data is None:
            data = ""
        sys.stdout.write(str(data) + "\n")
