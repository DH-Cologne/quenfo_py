""" __init__-Script to manage Settings of ArgParser-arguments and config.yaml-settings."""

# ## Imports
from configuration.config_model import Configurations

# ## Define Variables
config_obj = None


# ## Function
def set_config(method_args: dict) -> None:
    """ Function manages the Settings for Configuration-object.
            a. gets values from ArgumentParser (input_path and db_mode)
            b. gets values from configuration file 
        --> Setters are used to check if values are valid. """

    # Set global
    global config_obj

    # ArgParser Settings
    input_path = method_args['input_path']  # extract input_path from argparser
    db_mode = method_args['db_mode']  # extract new db_mode from argparser
    config_obj = Configurations(input_path,
                                db_mode)  # instantiate config_obj and pass vars input_path and db_mode from argparser
    config_obj.set_input_path()
    config_obj.set_mode()

    # Configuration-File Settings
    config_obj.set_fetch_size()  # check and set data-handling values
    config_obj.set_query_limit()  #
    config_obj.set_start_pos()  #

    # Classification
    config_obj.set_fus_config()  # check and set specific training and processing values
    config_obj.set_knn_config()  #
    config_obj.set_tfidf_config()  #

    config_obj.set_knn_path()  # check and set classification paths
    config_obj.set_tfidf_path()  #
    config_obj.set_traindata_path()  #
    config_obj.set_regex_path()  #
    config_obj.set_stopwords_path()  #

    # IE
    config_obj.set_ie_type()    # check and set ie config values
    config_obj.set_expand_coordinates()
    config_obj.set_search_type()

    config_obj.set_competence_paths()   # check and set ie paths
    config_obj.set_tool_paths()
