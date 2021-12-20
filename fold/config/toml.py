import toml

from fold import ConfigParser


class TOMLConfigParser(ConfigParser):
    @classmethod
    def fromText(cls, text: str) -> dict:
        return toml.loads(text)
