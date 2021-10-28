import unittest

from information_extraction.prepare_resources.connection_resources import read_failures, read_pattern_from_file


class TestGetResourceFile(unittest.TestCase):

    def test_get_entities_from_file(self):
        self.assertIsNotNone(read_failures("competences"))
        self.assertIsNotNone(read_failures("no_competences"))
        self.assertIsNotNone(read_failures("tools"))
        self.assertIsNotNone(read_failures("no_tools"))
        self.assertIsNotNone(read_failures("modifier"))

        self.assertIsInstance(read_failures("competences"), list)
        self.assertIsInstance(read_failures("no_competences"), list)
        self.assertIsInstance(read_failures("tools"), list)
        self.assertIsInstance(read_failures("no_tools"), list)
        self.assertIsInstance(read_failures("modifier"), list)

    def test_get_pattern_from_file(self):
        self.assertIsNotNone(read_pattern_from_file("comp_pattern"))
        self.assertIsNotNone(read_pattern_from_file("tool_pattern"))

        self.assertIsInstance(read_pattern_from_file("comp_pattern"), list)
        self.assertIsInstance(read_pattern_from_file("tool_pattern"), list)


if __name__ == '__main__':
    unittest.main()