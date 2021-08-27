from classification.predict_classes.knn_predictor import gen_classes
from configuration.config_model import Configurations
from . import gen_regex

def call_regex_clf():
    regex_path = Configurations.get_regex_path()
    regex_clf = gen_regex.start(regex_path)
    return regex_clf