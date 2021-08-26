import yaml
from pathlib import Path

# Configuration Class
class Configurations():
    """ Class to get the parameters set in config.yaml and check if they are valid. 
        --> If not, set default values. """
        
    # ## Open Configuration-file and set variables + paths
    with open(Path('configuration/config.yaml'), 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
        models = cfg['models']
        fus_config = cfg['fus_config']
        query_limit = cfg['query_limit']
        mode = cfg['mode']
        tfidf_path = models['tfidf_path']
        knn_path = models['knn_path']
        tfidf_config = cfg['tfidf_config']
        knn_config = cfg['knn_config']
        resources = cfg['resources']
        traindata_path = resources['traindata_path']
        input_path = resources['input_path']
        stopwords_path = resources['stopwords_path']

    # Getter
    def get_traindata_path(): 
        traindata_path = Configurations.traindata_path
        return Configurations.__check_path(traindata_path)
    def get_tfidf_path(): 
        tfidf_path = Configurations.tfidf_path
        return Configurations.__check_path(tfidf_path)
    def get_knn_path(): 
        knn_path = Configurations.knn_path
        return Configurations.__check_path(knn_path)
    def get_input_path(): 
        input_path = Configurations.input_path
        return Configurations.__check_path(input_path)
    def get_stopwords_path(): 
        stopwords_path = Configurations.stopwords_path
        return Configurations.__check_path(stopwords_path)
    def get_query_limit():
        query_limit = Configurations.query_limit
        print(type(query_limit))
        return Configurations.__check_type(query_limit, 50, int)
    def get_mode():
        mode = Configurations.mode
        return Configurations.__check_strings(mode, 'overwrite', ('append', 'overwrite'))
    def get_tfidf_config():
        tfidf_config = Configurations.tfidf_config
        if tfidf_config == None:
            tfidf_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        # give dictionary, key to check, defaultvalue if given value is wrong and type to check
        # logging info: default wurde genutzt weil input falscher typ etc.
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'lowercase', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'max_df', 1.0, float)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'min_df', 1, int)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'sublinear_tf', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'use_idf', True, bool)
        return tfidf_config
    def get_fus_config():
        fus_config = Configurations.fus_config
        if fus_config == None:
            fus_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        fus_config = Configurations.__check_type_for_dict(fus_config, 'normalize', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'stem', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'filterSW', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'nGrams', {3,4}, dict)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'continuousNGrams', False, bool)
        return fus_config
    def get_knn_config():
        knn_config = Configurations.knn_config
        if knn_config == None:
            knn_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        # give dictionary, key to check, defaultvalue if given value is wrong and type to check
        knn_config = Configurations.__check_type_for_dict(knn_config, 'n_neighbors', 5, int)
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'weights', 'uniform', ('uniform', 'distance'))
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'algorithm', 'auto', ('auto', 'ball_tree', 'kd_tree', 'brute'))
        knn_config = Configurations.__check_type_for_dict(knn_config, 'leaf_size', 30, int)
        return knn_config
    
    # Checker + Default Setter
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