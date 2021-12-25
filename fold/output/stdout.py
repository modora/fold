from typing import Any, Optional
import sys

from .common import OutputPlugin, Content


class StdoutOutputPlugin(OutputPlugin):
    NAME = "stdout"

    def __init__(self, config: Optional[Content]) -> None:
        super().__init__(config)

    @classmethod
    def parseConfig(cls, config: Optional[Content]) -> Optional[Content]:
        return super().parseConfig(config)

    def write(self, data: Any):
        sys.stdout.write(str(data) + "\n")
