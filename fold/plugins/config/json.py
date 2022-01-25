from typing import Dict
import json

from fold.core import Content
from .common import ConfigFilePlugin


class JSONConfig(ConfigFilePlugin):
    EXTENSIONS = {"json"}

    @classmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        return json.loads(text)
