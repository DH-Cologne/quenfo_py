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

    def test_start_pos(self):
        start_pos = cfg['classification']['start_pos']
        self.assertNotIsInstance(start_pos, (str, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                      "start_pos is"
                                                                                                      " not integer.")
        self.assertIsInstance(start_pos, int)

    def test_stopwords_path(self):
        stopwords = cfg['resources']['stopwords_path']
        self.assertNotIsInstance(stopwords, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "stopwords-path is"
                                                                                                    " not string.")
        self.assertIsInstance(stopwords, str)
        self.assertRegex(stopwords, ".*txt$", "Path does not end with string 'txt'.")

    def test_regex_path(self):
        regex = cfg['resources']['regex_path']
        self.assertNotIsInstance(regex, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "regex-path is"
                                                                                                    " not string.")
        self.assertIsInstance(regex, str)
        self.assertRegex(regex, ".*txt$", "Path does not end with string 'txt'.")

    def test_traindata_path(self):
        traindata = cfg['resources']['traindata_path']
        self.assertNotIsInstance(traindata, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "traindata-path is"
                                                                                                    " not string.")
        self.assertIsInstance(traindata, str)
        self.assertRegex(traindata, ".*db$", "Path does not end with string 'db'.")

    def test_tfidf_path(self):
        tfidf = cfg['classification']['models']['tfidf_path']
        self.assertNotIsInstance(tfidf, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "tfidf-path is"
                                                                                                    " not string.")
        self.assertIsInstance(tfidf, str)
        #self.assertRegex(tfidf, ".*pkl$", "Path does not end with string 'pkl'.")

    def test_knn_path(self):
        knn = cfg['classification']['models']['knn_path']
        self.assertNotIsInstance(knn, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                                    "knn-path is"
                                                                                                    " not string.")
        self.assertIsInstance(knn, str)
        #self.assertRegex(knn, ".*pkl$", "Path does not end with string 'pkl'.")

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

    
    def test_tfidf_config_values(self):
        lowercase = cfg['classification']['tfidf_config']['lowercase']
        max_df = cfg['classification']['tfidf_config']['max_df']
        min_df = cfg['classification']['tfidf_config']['min_df']
        sublinear_tf = cfg['classification']['tfidf_config']['sublinear_tf']
        use_idf = cfg['classification']['tfidf_config']['use_idf']

        self.assertIsInstance(lowercase, bool, "Type of lowercase-configuration is not boolean.")
        self.assertIsInstance(max_df, float, "Type of max_df-configuration is not float.")
        self.assertIsInstance(min_df, int, "Type of min_df-configuration is not int.")
        self.assertIsInstance(sublinear_tf, bool, "Type of sublinear_tf-configuration is not boolean.")
        self.assertIsInstance(use_idf, bool, "Type of use_idf-configuration is not boolean.")

    def test_knn_config_values(self):
        n_neighbors = cfg['classification']['knn_config']['n_neighbors']
        leaf_size = cfg['classification']['knn_config']['leaf_size']
        weights = cfg['classification']['knn_config']['weights']
        algorithm = cfg['classification']['knn_config']['algorithm']

        self.assertIsInstance(n_neighbors, int, "Type of n_neighbors-config is not int.")
        self.assertIsInstance(leaf_size, int, "Type of leaf_size-config is not int.")
        self.assertTrue(any(i in (weights) for i in ('uniform', 'distance')))
        self.assertTrue(any(i in (algorithm) for i in ('auto', 'ball_tree', 'kd_tree', 'brute')))
        
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
