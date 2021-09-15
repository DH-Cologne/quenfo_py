# ## Imports
import ruamel.yaml
from pathlib import Path

# Configuration Class
class Configurations:
    """ Class to get the parameters set in config.yaml and check if they are valid. 
        --> If not, set default values. """
    def __init__(self, arg_input_path, arg_db_mode):
        # ## Open Configuration-file and set variables + paths
        with open(Path('configuration/config.yaml'), 'r') as yamlfile:
            yaml = ruamel.yaml.YAML(typ='safe')
            cfg = yaml.load(yamlfile)
            fus_config = cfg['Classification']['fus_config']
            query_limit = cfg['Classification']['query_limit']
            fetch_size = cfg['Classification']['fetch_size']
            start_pos = cfg['Classification']['start_pos']
            tfidf_path = cfg['Classification']['models']['tfidf_path']
            knn_path = cfg['Classification']['models']['knn_path']
            tfidf_config = cfg['Classification']['tfidf_config']
            knn_config = cfg['Classification']['knn_config']
            traindata_path = cfg['resources']['traindata_path']
            stopwords_path = cfg['resources']['stopwords_path']
            regex_path = cfg['resources']['regex_path']
        # Set default values
        self.fus_config = fus_config
        self.query_limit = query_limit
        self.fetch_size = fetch_size
        self.start_pos = start_pos
        self.tfidf_path = tfidf_path
        self.knn_path = knn_path
        self.tfidf_config = tfidf_config
        self.knn_config = knn_config
        self.traindata_path = traindata_path
        self.stopwords_path = stopwords_path
        self.regex_path = regex_path
        self.db_mode = arg_db_mode
        self.input_path = arg_input_path

    # Setter
    def set_traindata_path(self):
        traindata_path = Configurations.__check_path(self.traindata_path)
        self.traindata_path = traindata_path
    def set_tfidf_path(self):
        tfidf_path = Configurations.__check_path(self.tfidf_path)
        self.tfidf_path = tfidf_path
    def set_knn_path(self):
        knn_path = Configurations.__check_path(self.knn_path)
        self.knn_path = knn_path
    def set_input_path(self):
        input_path = Configurations.__check_path(self.input_path)
        self.input_path = input_path
    def set_stopwords_path(self):
        stopwords_path = Configurations.__check_path(self.stopwords_path)
        self.stopwords_path = stopwords_path
    def set_regex_path(self):
        regex_path = Configurations.__check_path(self.regex_path)
        self.regex_path = regex_path
    def set_query_limit(self):
        query_limit = Configurations.__check_type(self.query_limit, 50, int)
        self.query_limit = query_limit
    def set_fetch_size(self):
        fetch_size = Configurations.__check_type(self.fetch_size, 500, int)
        self.fetch_size = fetch_size
    def set_start_pos(self):
        start_pos = Configurations.__check_type(self.start_pos, 0, int)
        self.start_pos = start_pos
    def set_mode(self):
        db_mode = Configurations.__check_strings(self.db_mode, 'overwrite', ('append', 'overwrite'))
        self.db_mode = db_mode

    def set_tfidf_config(self) -> dict:
        tfidf_config = self.tfidf_config
        if tfidf_config == None:
            tfidf_config = dict()
        # Check-functions to avoid error raises because of missing or wrong inputs
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'lowercase', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'max_df', 1.0, float)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'min_df', 1, int)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'sublinear_tf', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'use_idf', True, bool)
        self.tfidf_config = tfidf_config

    def set_fus_config(self) -> dict:
        fus_config = self.fus_config
        if fus_config == None:
            fus_config = dict()
        # Check-functions to avoid error raises because of missing or wrong inputs
        fus_config = Configurations.__check_type_for_dict(fus_config, 'normalize', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'stem', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'filterSW', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'nGrams', {3,4}, dict)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'continuousNGrams', False, bool)
        self.fus_config = fus_config

    def set_knn_config(self) -> dict:
        knn_config = self.knn_config
        if knn_config == None:
            knn_config = dict()
        # Check-functions to avoid error raises because of missing or wrong inputs
        knn_config = Configurations.__check_type_for_dict(knn_config, 'n_neighbors', 5, int)
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'weights', 'uniform', ('uniform', 'distance'))
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'algorithm', 'auto', ('auto', 'ball_tree', 'kd_tree', 'brute'))
        knn_config = Configurations.__check_type_for_dict(knn_config, 'leaf_size', 30, int)
        self.knn_config = knn_config
    
    # Getter
    def get_traindata_path(self) -> str: 
        return self.traindata_path
    def get_tfidf_path(self) -> str: 
        return self.tfidf_path
    def get_knn_path(self) -> str: 
        return self.knn_path
    def get_input_path(self) -> str: 
        return self.input_path
    def get_stopwords_path(self) -> str: 
        return self.stopwords_path
    def get_regex_path(self) -> str: 
        return self.regex_path
    def get_query_limit(self) -> int:
        return self.query_limit
    def get_fetch_size(self) -> int:
        return self.fetch_size
    def get_start_pos(self) -> int:
        return self.start_pos
    def get_mode(self) -> str:
        return self.db_mode
    def get_tfidf_config(self) -> dict:
        return self.tfidf_config
    def get_fus_config(self) -> dict:
        return self.fus_config
    def get_knn_config(self) -> dict:
        return self.knn_config
    
    # Checker
    def __check_path(path):
        try:
            Path(path).exists()
            path = path
        except FileNotFoundError:
            path = None
        return path

    def __check_type_for_dict(current_dict, key, default_val, type_input):
        try:
            if type(current_dict[key]) != type_input:
                raise KeyError
        except KeyError:
            try:
                current_dict[key] = default_val
            except KeyError:
                current_dict.update({key: default_val})
        return current_dict

    def __check_type(val_to_check, default_val, type_input):
        try:
            if type(val_to_check) != type_input:
                raise KeyError
        except KeyError:
            val_to_check = default_val
        return val_to_check

    def __check_strings(str_to_check, default_str, choices):
        try:
            if [s for s in choices if str(str_to_check) in s] == []:
                raise KeyError
        except KeyError:
            str_to_check = default_str
        return str_to_check

    def __check_strings_for_dict(current_dict, key, default_str, choices):
        str_to_check = current_dict[key]
        try:
            if [s for s in choices if str(str_to_check) in s] == []:
                raise KeyError
        except KeyError:
            try:
                current_dict[key] = default_str
            except KeyError:
                current_dict.update({key: default_str})
        return current_dict