from configuration.config_model import Configurations
config_obj = None

def set_config(method_args):
    global config_obj
    input_path = method_args['input_path']                  # set new input_path from argparser
    db_mode = method_args['db_mode']                        # set new db_mode from argparser
    
    config_obj = Configurations(input_path, db_mode)        # instantiate config_obj and pass vars input_path and db_mode from argparser    
    config_obj.set_fetch_size()                             # extract config.yaml-value --> check and set fetch_size 
    config_obj.set_fus_config()
    config_obj.set_input_path()
    config_obj.set_knn_config()
    config_obj.set_knn_path()
    config_obj.set_mode()
    config_obj.set_query_limit()
    config_obj.set_regex_path()
    config_obj.set_start_pos()
    config_obj.set_stopwords_path()
    config_obj.set_tfidf_config()
    config_obj.set_tfidf_path()
    config_obj.set_mode()