import unittest
import fold.utils


class TestModuleObjectStringParser(unittest.TestCase):
    def _test(self, string, expected):
        result = fold.utils.parseModuleObjectString(string)

        self.assertTupleEqual(expected, result)

    def _testRaises(self, exception, string):
        self.assertRaises(exception, fold.utils.parseModuleObjectString, string)

    def testSysStdout(self):
        string = "sys/stdout"
        expected = ("sys", "stdout")

        self._test(string, expected)

    def testOSPathAbspath(self):
        string = "os.path/abspath"
        expected = ("os.path", "abspath")

        self._test(string, expected)

    def testTyping(self):
        """This test should fail since no object is present"""
        string = "typing"
        self._testRaises(ValueError, string)
