from typing import Any, Optional, TypedDict
import sys

from .common import OutputPlugin, Content


class StdoutOutputPlugin(OutputPlugin):
    NAME = "stdout"

    def __init__(self, config: Optional[Content]) -> None:
        super().__init__(config)

    @classmethod
    def parseConfig(cls, config: Optional[Content]) -> None:
        # It's stdout... there is no configuration. Just ignore everything
        return None

    def write(self, data: Any):
        sys.stdout.write(str(data) + "\n")
