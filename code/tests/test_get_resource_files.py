import unittest
from pathlib import Path

import yaml

from information_extraction.prepare_resources.connection_resources import get_entities_from_file

with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)


class TestGetResourceFile(unittest.TestCase):
    # get path from config
    # competences
    competence_path = cfg['resources']['competences_path']
    no_competence_path = cfg['resources']['nocompetences_path']
    modifier_path = cfg['resources']['modifier_path']
    comppattern_path = cfg['resources']['comppattern_path']

    # tools
    tools_path = cfg['resources']['tools_path']
    no_tools_path = cfg['resources']['notools_path']
    toolpattern_path = cfg['resources']['toolpattern_path']

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
