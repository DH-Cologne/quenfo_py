import unittest
from pathlib import Path

import yaml

with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)


class TestConfiguration(unittest.TestCase):
    def test_query_limit(self):
        query_limit = cfg['query_limit']
        self.assertNotIsInstance(query_limit, (str, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                      "query_limit is"
                                                                                                      " not integer.")
        self.assertIsInstance(query_limit, int)

    def test_db_path(self):
        path = cfg['resources']['input_path']
        self.assertNotIsInstance(path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                               "db-path is"
                                                                                               " not string.")
        self.assertIsInstance(path, str)
        self.assertRegex(path, ".*db$", "Path does not end with string 'db' and is not the path to a database.")

    def test_stopwords_path(self):
        stopwords = cfg['resources']['stopwords_path']
        self.assertNotIsInstance(stopwords, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "stopwords-path is"
                                                                                                    " not string.")
        self.assertIsInstance(stopwords, str)
        self.assertRegex(stopwords, ".*txt$", "Path does not end with string 'txt'.")

    def test_fu_config_values(self):
        normalize = cfg['fus_config']['normalize']
        stem = cfg['fus_config']['stem']
        filter_sw = cfg['fus_config']['filterSW']
        ngrams = cfg['fus_config']['nGrams']
        cngrams = cfg['fus_config']['continuousNGrams']

        self.assertIsInstance(normalize, bool, "Type of normalize-configuration is not boolean.")
        self.assertIsInstance(stem, bool, "Type of stemming-configuration is not boolean.")
        self.assertIsInstance(filter_sw, bool, "Type of stopword-filter-configuration is not boolean.")
        self.assertIsInstance(cngrams, bool, "Type of continuous-ngram-configuration is not boolean.")
        self.assertIsInstance(ngrams, dict, "Type of ngram-configuration is not dictionary.")


if __name__ == '__main__':
    unittest.main()
