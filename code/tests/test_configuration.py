import unittest
from pathlib import Path

import yaml

with open(Path('C:\\Users\Anne\Desktop\Quenfo\quenfo_py_data\config\config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)


class TestConfiguration(unittest.TestCase):
    def test_query_limit(self):
        query_limit = cfg['classification']['query_limit']
        self.assertNotIsInstance(query_limit, (str, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                      "query_limit is"
                                                                                                      " not integer.")
        self.assertIsInstance(query_limit, int)

    def test_fetch_size(self):
        fetch_size = cfg['classification']['fetch_size']
        self.assertNotIsInstance(fetch_size, (str, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                      "fetch_size is"
                                                                                                      " not integer.")
        self.assertIsInstance(fetch_size, int)

    """ def test_db_path(self):
        path = cfg['resources']['input_path']
        self.assertNotIsInstance(path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                               "db-path is"
                                                                                               " not string.")
        self.assertIsInstance(path, str)
        self.assertRegex(path, ".*db$", "Path does not end with string 'db' and is not the path to a database.") """

    def test_stopwords_path(self):
        stopwords = cfg['resources']['stopwords_path']
        self.assertNotIsInstance(stopwords, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "stopwords-path is"
                                                                                                    " not string.")
        self.assertIsInstance(stopwords, str)
        self.assertRegex(stopwords, ".*txt$", "Path does not end with string 'txt'.")

    def test_fu_config_values(self):
        normalize = cfg['classification']['fus_config']['normalize']
        stem = cfg['classification']['fus_config']['stem']
        filter_sw = cfg['classification']['fus_config']['filterSW']
        ngrams = cfg['classification']['fus_config']['nGrams']
        cngrams = cfg['classification']['fus_config']['continuousNGrams']

        self.assertIsInstance(normalize, bool, "Type of normalize-configuration is not boolean.")
        self.assertIsInstance(stem, bool, "Type of stemming-configuration is not boolean.")
        self.assertIsInstance(filter_sw, bool, "Type of stopword-filter-configuration is not boolean.")
        self.assertIsInstance(cngrams, bool, "Type of continuous-ngram-configuration is not boolean.")
        self.assertIsInstance(ngrams, dict, "Type of ngram-configuration is not dictionary.")

    def test_ie_paths(self):
        competences_path = cfg['resources']['competences_path']
        nocompetences_path = cfg['resources']['nocompetences_path']
        comppattern_path = cfg['resources']['comppattern_path']
        modifier_path = cfg['resources']['modifier_path']
        tools_path = cfg['resources']['tools_path']
        notools_path = cfg['resources']['notools_path']
        toolpattern_path = cfg['resources']['toolpattern_path']

        self.assertNotIsInstance(competences_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of competences-path is not string.")
        self.assertNotIsInstance(nocompetences_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of nocompetences-path is not string.")
        self.assertNotIsInstance(comppattern_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of comppattern-path is not string.")
        self.assertNotIsInstance(modifier_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                        "modifier"
                                                                                                        "-path is not "
                                                                                                        "string.")
        self.assertNotIsInstance(toolpattern_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of toolpattern-path is not string.")
        self.assertNotIsInstance(tools_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                     "tool-path is "
                                                                                                     "not string.")
        self.assertNotIsInstance(notools_path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                       "notool-path "
                                                                                                       "is not "
                                                                                                       "string.")

        self.assertIsInstance(competences_path, str)
        self.assertIsInstance(nocompetences_path, str)
        self.assertIsInstance(comppattern_path, str)
        self.assertIsInstance(modifier_path, str)
        self.assertIsInstance(tools_path, str)
        self.assertIsInstance(notools_path, str)
        self.assertIsInstance(toolpattern_path, str)

        self.assertRegex(competences_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(nocompetences_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(comppattern_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(modifier_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(tools_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(notools_path, ".*txt$", "Path does not end with string 'txt'.")
        self.assertRegex(toolpattern_path, ".*txt$", "Path does not end with string 'txt'.")


if __name__ == '__main__':
    unittest.main()
