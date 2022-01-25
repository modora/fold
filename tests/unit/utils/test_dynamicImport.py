import unittest

from fold.utils.imp import importFromString


class TestStringImporter(unittest.TestCase):
    def testImportMath(self):
        import math as expected

        name = "math"
        result = importFromString(name)
        self.assertEqual(expected, result)

    def testImportOsPath(self):
        import os.path as expected

        name = "os.path"
        result = importFromString(name)
        self.assertEqual(expected, result)

    def testFromPathlibImportPath(self):
        from pathlib import Path as expected

        name = "pathlib:Path"
        result = importFromString(name)
        self.assertEqual(expected, result)

    def testFromJSONImportDecoderJSONDecodeError(self):
        from json.decoder import JSONDecodeError as expected

        name = "json:decoder.JSONDecodeError"
        result = importFromString(name)
        self.assertEqual(expected, result)
