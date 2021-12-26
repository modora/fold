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
