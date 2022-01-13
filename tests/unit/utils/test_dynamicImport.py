import unittest

from fold.utils.dynamicImport import loadObjectDynamically


class TestDynamicLoader(unittest.TestCase):
    def testImportMath(self):
        import math as expected

        name = "math"
        result = loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testImportOsPath(self):
        import os.path as expected

        name = "os.path"
        result = loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testFromPathlibImportPath(self):
        from pathlib import Path as expected

        name = "pathlib:Path"
        result = loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testFromJSONImportDecoderJSONDecodeError(self):
        from json.decoder import JSONDecodeError as expected

        name = "json:decoder.JSONDecodeError"
        result = loadObjectDynamically(name)
        self.assertEqual(expected, result)
