import json

from fold import ConfigParser


class JSONConfigParser(ConfigParser):
    @classmethod
    def fromText(cls, text: str) -> dict:
        return json.loads(text)
