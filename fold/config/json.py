from typing import Dict
import json

from .common import ConfigFilePlugin, Content


class JSONConfig(ConfigFilePlugin):
    EXTENSIONS = {"json"}

    @classmethod
    def fromText(cls, text: str) -> Dict[str, Content]:
        return json.loads(text)
