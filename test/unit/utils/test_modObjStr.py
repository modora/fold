import unittest

from fold.utils.stringParser import parseModuleObjectString, parseObjectAttrString


class TestModuleObjectStringParser(unittest.TestCase):
    def _test(self, string, expected):
        result = parseModuleObjectString(string)

        self.assertTupleEqual(expected, result)

    def _testRaises(self, exception, string):
        self.assertRaises(exception, parseModuleObjectString, string)

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
        expected = (".module", None)

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
        result = parseObjectAttrString(name)
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
