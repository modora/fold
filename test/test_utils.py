import unittest
import fold.utils


class TestModuleObjectStringParser(unittest.TestCase):
    def _test(self, string, expected):
        result = fold.utils.parseModuleObjectString(string)

        self.assertTupleEqual(expected, result)

    def _testRaises(self, exception, string):
        self.assertRaises(exception, fold.utils.parseModuleObjectString, string)

    def testModule(self):
        string = "module"
        expected = ("module", None)

        self._test(string, expected)

    def testModuleSubmodule(self):
        string = "module.submodule"
        expected = ("module.submodule", None)

        self._test(string, expected)

    def testModuleSubmodule(self):
        string = "module.submodule"
        expected = ("module.submodule", None)

        self._test(string, expected)

    def testModuleObject(self):
        string = "module:object"
        expected = ("module", "object")

        self._test(string, expected)

    def testModuleSubmoduleObject(self):
        string = "module.submodule:object"
        expected = ("module.submodule", "object")

        self._test(string, expected)

    def testModuleObjectAttr(self):
        string = "module:object.attr"
        expected = ("module", "object.attr")

        self._test(string, expected)

    def testModuleSubmoduleObjectAttr(self):
        string = "module.submodule:object.attr"
        expected = ("module.submodule", "object.attr")

        self._test(string, expected)

    def testColonModule(self):
        string = ":module"
        expected = ValueError

        self._testRaises(expected, string)

    def testObjectNotDefined(self):
        string = "module:"
        expected = ("module", None)

        self._test(string, expected)

    def testRelativeModule(self):
        """We are allowing relative imports"""
        string = ".module"
        expected = (".module", None)

        self._test(string, expected)

    def testModuleDot(self):
        string = "module."
        expected = ("module", None)

        self._test(string, expected)

    def testDotModuleDot(self):
        string = ".module."
        expected = ("module", None)

        self._test(string, expected)

    def testDotObject(self):
        string = "module:.object"
        expected = ("module", "object")

        self._test(string, expected)

    def testObjectDot(self):
        string = "module:object."
        expected = ("module", "object")

        self._test(string, expected)

    def testDotObjectDot(self):
        string = "module:.object."
        expected = ("module", "object")

        self._test(string, expected)


class TestObjectStringParser(unittest.TestCase):
    def _test(self, expected, name):
        result = fold.utils.parseObjectString(name)
        self.assertTupleEqual(expected, result)

    def testObject(self):
        name = "object"
        expected = ("object", [])

        self._test(expected, name)

    def testObjectAttr(self):
        name = "object.attr"
        expected = ("object", ["attr"])

        self._test(expected, name)

    def testObjectAttrSubattr(self):
        name = "object.attr.subattr"
        expected = ("object", ["attr", "subattr"])

        self._test(expected, name)


class TestDynamicLoader(unittest.TestCase):
    def testImportMath(self):
        import math as expected

        name = "math"
        result = fold.utils.loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testImportOsPath(self):
        import os.path as expected

        name = "os.path"
        result = fold.utils.loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testFromPathlibImportPath(self):
        from pathlib import Path as expected

        name = "pathlib:Path"
        result = fold.utils.loadObjectDynamically(name)
        self.assertEqual(expected, result)

    def testFromJSONImportDecoderJSONDecodeError(self):
        from json.decoder import JSONDecodeError as expected

        name = "json:decoder.JSONDecodeError"
        result = fold.utils.loadObjectDynamically(name)
        self.assertEqual(expected, result)
