import unittest

from information_extraction.prepare_resources.connection_resources import get_entities_from_file, read_pattern_from_file


class TestGetResourceFile(unittest.TestCase):

    def test_get_entities_from_file(self):
        self.assertIsNotNone(get_entities_from_file("competences"))
        self.assertIsNotNone(get_entities_from_file("no_competences"))
        self.assertIsNotNone(get_entities_from_file("tools"))
        self.assertIsNotNone(get_entities_from_file("no_tools"))
        self.assertIsNotNone(get_entities_from_file("modifier"))

        self.assertIsInstance(get_entities_from_file("competences"), list)
        self.assertIsInstance(get_entities_from_file("no_competences"), list)
        self.assertIsInstance(get_entities_from_file("tools"), list)
        self.assertIsInstance(get_entities_from_file("no_tools"), list)
        self.assertIsInstance(get_entities_from_file("modifier"), list)

    def test_get_pattern_from_file(self):
        self.assertIsNotNone(read_pattern_from_file("comp_pattern"))
        self.assertIsNotNone(read_pattern_from_file("tool_pattern"))

        self.assertIsInstance(read_pattern_from_file("comp_pattern"), list)
        self.assertIsInstance(read_pattern_from_file("tool_pattern"), list)


if __name__ == '__main__':
    unittest.main()