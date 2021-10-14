# ## Imports
import ruamel.yaml
from pathlib import Path
import os
import logger


# Configuration Class
class Configurations:
    """ Class to get the parameters set in config.yaml and check if they are valid. 
        --> If not, set default values. """

    def __init__(self, arg_input_path, arg_db_mode):

        # Get global_path (relative for all other needed files) from input_file
        global_path = extract_globalpath(arg_input_path)

        # ## Open Configuration-file and set variables + paths
        with open(Path(os.path.join(global_path, 'config/config.yaml')), 'r') as yamlfile:
            yaml = ruamel.yaml.YAML(typ='safe')
            cfg = yaml.load(yamlfile)
            # classification config
            fus_config = cfg['classification']['fus_config']
            c_query_limit = cfg['classification']['query_limit']
            c_fetch_size = cfg['classification']['fetch_size']
            c_start_pos = cfg['classification']['start_pos']
            # model paths
            tfidf_path = os.path.join(global_path, 'resources', cfg['classification']['models']['tfidf_path'])
            knn_path = os.path.join(global_path, 'resources', cfg['classification']['models']['knn_path'])
            # config modeling
            tfidf_config = cfg['classification']['tfidf_config']
            knn_config = cfg['classification']['knn_config']
            # resources
            global_resources = [global_path, 'resources','classification']                               # subfolder resources
            traindata_path = os.path.join(*global_resources, 'trainingSets', cfg['resources']['traindata_path'])
            stopwords_path = os.path.join(*global_resources, cfg['resources']['stopwords_path'])
            regex_path = os.path.join(*global_resources, cfg['resources']['regex_path'])

            # ie config
            ie_query_limit = cfg['ie_config']['query_limit']
            ie_fetch_size = cfg['ie_config']['fetch_size']
            ie_start_pos = cfg['ie_config']['start_pos']
            expand_coordinates = cfg['ie_config']['expand_coordinates']
            search_type = cfg['ie_config']['search']
            ie_type = cfg['ie_config']['type']

            # competence paths
            global_comp = [global_path, 'resources','information_extraction','competences']         # subfolder for competences
            competence_path = os.path.join(*global_comp, cfg['resources']['competences_path'])
            no_competence_path = os.path.join(*global_comp, cfg['resources']['nocompetences_path'])
            modifier_path = os.path.join(*global_comp, cfg['resources']['modifier_path'])
            comppattern_path = os.path.join(*global_comp, cfg['resources']['comppattern_path'])

            # tool paths
            global_tools = [global_path, 'resources','information_extraction','tools']              # subfolder for tools
            tool_path = os.path.join(*global_tools, cfg['resources']['tools_path'])
            no_tools_path = os.path.join(*global_tools, cfg['resources']['notools_path'])
            toolpattern_path = os.path.join(*global_tools, cfg['resources']['toolpattern_path'])

            # compounds paths
            global_comps = [global_path, 'resources', 'nlp', 'compounds']                           # subfolder for compounds
            possible_comps = os.path.join(*global_comps, cfg['resources']['possible_comp_path'])
            splitted_comps = os.path.join(*global_comps, cfg['resources']['splitted_comp_path'])

        # Set default values
        # classification
        self.fus_config = fus_config
        self.c_query_limit = c_query_limit
        self.c_fetch_size = c_fetch_size
        self.c_start_pos = c_start_pos
        self.tfidf_path = tfidf_path
        self.knn_path = knn_path
        self.tfidf_config = tfidf_config
        self.knn_config = knn_config
        self.traindata_path = traindata_path
        self.stopwords_path = stopwords_path
        self.regex_path = regex_path

        # ie
        self.ie_query_limit = ie_query_limit
        self.ie_fetch_size = ie_fetch_size
        self.ie_start_pos = ie_start_pos
        self.expand_coordinates = expand_coordinates
        self.search_type = search_type
        self.ie_type = ie_type
        self.competence_path = competence_path
        self.no_competence_path = no_competence_path
        self.modifier_path = modifier_path
        self.comppattern_path = comppattern_path
        self.tool_path = tool_path
        self.no_tools_path = no_tools_path
        self.toolpattern_path = toolpattern_path
        self.possible_comps = possible_comps
        self.splitted_comps = splitted_comps

        # Values passed by ArgumentParser
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
        c_query_limit = Configurations.__check_type(self.c_query_limit, 50, int)
        ie_query_limit = Configurations.__check_type(self.ie_query_limit, 50, int)
        self.c_query_limit = c_query_limit
        self.ie_query_limit = ie_query_limit

    def set_fetch_size(self):
        c_fetch_size = Configurations.__check_type(self.c_fetch_size, 500, int)
        ie_fetch_size = Configurations.__check_type(self.ie_fetch_size, 500, int)
        self.c_fetch_size = c_fetch_size
        self.ie_fetch_size = ie_fetch_size

    def set_start_pos(self):
        c_start_pos = Configurations.__check_type(self.c_start_pos, 0, int)
        ie_start_pos = Configurations.__check_type(self.ie_start_pos, 0, int)
        self.c_start_pos = c_start_pos
        self.ie_start_pos = ie_start_pos

    def set_mode(self):
        db_mode = Configurations.__check_strings(self.db_mode, 'overwrite', ('append', 'overwrite'))
        self.db_mode = db_mode

    def set_tfidf_config(self):
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

    def set_fus_config(self):
        fus_config = self.fus_config
        if fus_config is None:
            fus_config = dict()
        # Check-functions to avoid error raises because of missing or wrong inputs
        fus_config = Configurations.__check_type_for_dict(fus_config, 'normalize', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'stem', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'filterSW', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'nGrams', {3, 4}, dict)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'continuousNGrams', False, bool)
        self.fus_config = fus_config

    def set_knn_config(self):
        knn_config = self.knn_config
        if knn_config is None:
            knn_config = dict()
        # Check-functions to avoid error raises because of missing or wrong inputs
        knn_config = Configurations.__check_type_for_dict(knn_config, 'n_neighbors', 5, int)
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'weights', 'uniform', ('uniform', 'distance'))
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'algorithm', 'auto',
                                                             ('auto', 'ball_tree', 'kd_tree', 'brute'))
        knn_config = Configurations.__check_type_for_dict(knn_config, 'leaf_size', 30, int)
        self.knn_config = knn_config

    def set_expand_coordinates(self):
        expand_coordinates = Configurations.__check_type(self.expand_coordinates, True, bool)
        self.expand_coordinates = expand_coordinates

    def set_search_type(self):
        # TODO ClassIDs nochmal anpassen
        # standard value for tool extraction
        if "tools" in self.ie_type is True:
            self.search_type = 6

        # get value from config for competence extraction
        elif "competences" in self.ie_type is True and self.search_type is not None:
            search_type = Configurations.__check_type(self.search_type, 3, int)
            self.search_type = search_type

    def set_ie_type(self):
        ie_type = self.ie_type
        if ie_type is None:
            ie_type = dict()
        ie_type = Configurations.__check_type_for_dict(ie_type, 'competences', True, bool)
        ie_type = Configurations.__check_type_for_dict(ie_type, 'tools', False, bool)
        self.ie_type = ie_type

    def set_competence_paths(self):
        competence_path = Configurations.__check_path(self.competence_path)
        no_competence_path = Configurations.__check_path(self.no_competence_path)
        modifier_path = Configurations.__check_path(self.modifier_path)
        comppattern_path = Configurations.__check_path(self.comppattern_path)

        self.competence_path = competence_path
        self.no_competence_path = no_competence_path
        self.modifier_path = modifier_path
        self.comppattern_path = comppattern_path

    def set_tool_paths(self):
        tool_path = Configurations.__check_path(self.tool_path)
        no_tools_path = Configurations.__check_path(self.no_tools_path)
        toolpattern_path = Configurations.__check_path(self.toolpattern_path)

        self.tool_path = tool_path
        self.no_tools_path = no_tools_path
        self.toolpattern_path = toolpattern_path

    def set_pos_comps(self):
        possible_comps = Configurations.__check_path(self.possible_comps)
        self.possible_comps = possible_comps

    def set_split_comps(self):
        splitted_comps = Configurations.__check_path(self.splitted_comps)
        self.splitted_comps = splitted_comps

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

    def get_c_query_limit(self) -> int:
        return self.c_query_limit

    def get_c_fetch_size(self) -> int:
        return self.c_fetch_size

    def get_c_start_pos(self) -> int:
        return self.c_start_pos

    def get_mode(self) -> str:
        return self.db_mode

    def get_tfidf_config(self) -> dict:
        return self.tfidf_config

    def get_fus_config(self) -> dict:
        return self.fus_config

    def get_knn_config(self) -> dict:
        return self.knn_config

    def get_ie_start_pos(self) -> int:
        return self.ie_start_pos

    def get_ie_query_limit(self) -> int:
        return self.ie_query_limit

    def get_ie_fetch_size(self) -> int:
        return self.ie_fetch_size

    def get_expand_coordinates(self) -> bool:
        return self.expand_coordinates

    def get_search_type(self) -> int:
        return self.search_type

    def get_ie_type(self) -> dict:
        return self.ie_type

    def get_competences_path(self) -> str:
        return self.competence_path

    def get_no_competences_path(self) -> str:
        return self.no_competence_path

    def get_modifier_path(self) -> str:
        return self.modifier_path

    def get_comppattern_path(self) -> str:
        return self.comppattern_path

    def get_tool_path(self) -> str:
        return self.tool_path

    def get_no_tools_path(self) -> str:
        return self.no_tools_path

    def get_toolpattern_path(self) -> str:
        return self.toolpattern_path

    def get_pos_comps_path(self) -> str:
        return self.possible_comps

    def get_split_comps_path(self) -> str:
        return self.splitted_comps

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

def extract_globalpath(arg_input_path) -> str:
    try:
        global_path = os.path.join((arg_input_path.split('quenfo_py_data'))[0], 'quenfo_py_data')
        Path(global_path).exists()
        global_path = global_path
    except (FileNotFoundError, NotADirectoryError):
        global_path = None
        logger.log_main.error(f'Global_path {global_path} could not be resolved. Error was raised. Check again input_path.')
        print(f'Global_path {global_path} could not be resolved. Error was raised. Check again input_path.')
    return global_path