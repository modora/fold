import unittest

import fold.config


class TestTOMLConfigParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = fold.config.TOMLConfig

    def _test(self, content: str, expected: dict):
        actual = self.parser.fromText(content)

        self.assertDictEqual(actual, expected)

    def testEmptyFile(self):
        content = ""
        expected = {}

        self._test(content, expected)

    def testString(self):
        content = """
        foo = "bar"
        """
        expected = {"foo": "bar"}

        self._test(content, expected)

    def testStrings(self):
        content = """
        foo = "bar"
        hello = "world"
        """
        expected = {"foo": "bar", "hello": "world"}

        self._test(content, expected)

    def testDict(self):
        content = """
        [pokemon]
        pikachu = "electric"
        mew = "psychic"
        """
        expected = {"pokemon": {"pikachu": "electric", "mew": "psychic"}}

        self._test(content, expected)

    def testDicts(self):
        content = """
        [pokemon]
        pikachu = "electric"
        mew = "psychic"
        
        [superheros]
        batman = "DC"
        ironman = "Marvel"
        """

        expected = {
            "pokemon": {"pikachu": "electric", "mew": "psychic"},
            "superheros": {"batman": "DC", "ironman": "Marvel"},
        }

        self._test(content, expected)

    def testList(self):
        content = """
        shapes = ["square", "circle"]
        """
        expected = {"shapes": ["square", "circle"]}
        self._test(content, expected)

    def testLists(self):
        content = """
        shapes = ["square", "circle"]
        colors = ["red", "green", "blue"]
        """
        expected = {
            "shapes": ["square", "circle"],
            "colors": ["red", "green", "blue"],
        }

        self._test(content, expected)

    def testNestedDict(self):
        content = """
        [car]
        make = "Honda"
        model = "Civic"
        
        [car.position]
        x = 1
        y = 2
        """
        expected = {
            "car": {"make": "Honda", "model": "Civic", "position": {"x": 1, "y": 2}}
        }
        self._test(content, expected)

    def testListedDict(self):
        """Test list of dicts"""
        content = """
        [[employee]]
        name = "Bruce Wayne"
        occupation = "CEO"
        
        [[employee]]
        name = "Batman"
        occupation = "superhero"
        """

        expected = {
            "employee": [
                {"name": "Bruce Wayne", "occupation": "CEO"},
                {"name": "Batman", "occupation": "superhero"},
            ]
        }
        self._test(content, expected)

    def testListedDictReversed(self):
        """Test list of dicts checking if over is preserved"""
        content = """
        [[employee]]
        name = "Batman"
        occupation = "superhero"
        
        [[employee]]
        name = "Bruce Wayne"
        occupation = "CEO"
        
        """

        expected = {
            "employee": [
                {"name": "Batman", "occupation": "superhero"},
                {"name": "Bruce Wayne", "occupation": "CEO"},
            ]
        }
        self._test(content, expected)


class TestJSONConfigParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = fold.config.JSONConfig

    def _test(self, content: str, expected: dict):
        actual = self.parser.fromText(content)

        self.assertDictEqual(actual, expected)

    def testEmptyFile(self):
        content = "{}"
        expected = {}

        self._test(content, expected)

    def testString(self):
        content = """
        {"foo" : "bar"}
        """
        expected = {"foo": "bar"}

        self._test(content, expected)

    def testStrings(self):
        content = """
        {"foo": "bar", "hello": "world"}
        """
        expected = {"foo": "bar", "hello": "world"}

        self._test(content, expected)

    def testDict(self):
        content = """
        {"pokemon": {"pikachu": "electric", "mew": "psychic"}}
        """
        expected = {"pokemon": {"pikachu": "electric", "mew": "psychic"}}

        self._test(content, expected)

    def testDicts(self):
        content = """
        {
            "pokemon": {"pikachu": "electric", "mew": "psychic"},
            "superheros": {"batman": "DC", "ironman": "Marvel"}
        }
        """

        expected = {
            "pokemon": {"pikachu": "electric", "mew": "psychic"},
            "superheros": {"batman": "DC", "ironman": "Marvel"},
        }

        self._test(content, expected)

    def testList(self):
        content = """
        {"shapes": ["square", "circle"]}
        """
        expected = {"shapes": ["square", "circle"]}
        self._test(content, expected)

    def testLists(self):
        content = """
        {
            "shapes": ["square", "circle"],
            "colors": ["red", "green", "blue"]
        }
        """
        expected = {
            "shapes": ["square", "circle"],
            "colors": ["red", "green", "blue"],
        }

        self._test(content, expected)

    def testNestedDict(self):
        content = """
        {"car": {"make": "Honda", "model": "Civic", "position": {"x": 1, "y": 2}}}
        """
        expected = {
            "car": {"make": "Honda", "model": "Civic", "position": {"x": 1, "y": 2}}
        }
        self._test(content, expected)

    def testListedDict(self):
        """Test list of dicts"""
        content = """
        {
            "employee": [
                {"name": "Bruce Wayne", "occupation": "CEO"},
                {"name": "Batman", "occupation": "superhero"}
            ]
        }
        """

        expected = {
            "employee": [
                {"name": "Bruce Wayne", "occupation": "CEO"},
                {"name": "Batman", "occupation": "superhero"},
            ]
        }
        self._test(content, expected)

    def testListedDictReversed(self):
        """Test list of dicts checking if over is preserved"""
        content = """
        {
            "employee": [
                {"name": "Batman", "occupation": "superhero"},
                {"name": "Bruce Wayne", "occupation": "CEO"}
            ]
        }
        """

        expected = {
            "employee": [
                {"name": "Batman", "occupation": "superhero"},
                {"name": "Bruce Wayne", "occupation": "CEO"},
            ]
        }
        self._test(content, expected)
