from typing import Any
import sys

from .common import OutputPlugin


class StdoutOutputPlugin(OutputPlugin):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def write(self, data: Any):
        sys.stdout.write(str(data) + "\n")
