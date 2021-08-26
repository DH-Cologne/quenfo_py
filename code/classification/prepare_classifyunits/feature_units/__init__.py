# ## Imports
from orm_handling.models import Configurations
from . import convert_featureunits
from pathlib import Path

<<<<<<< HEAD:code/prepare_classifyunits/feature_units/__init__.py
# ## Open Configuration-file and set variables + paths
with open(Path(r'C:\Users\Christine\Documents\Qualifikationsentwicklungsforschung\quenfo\quenfo_py\code\config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    fus_config = cfg['fus_config']
    resources = cfg['resources']
=======
fus_config = Configurations.get_fus_config()
>>>>>>> bceb9509ac6ee5ff7264dc1f588c0754b26e3f34:code/classification/prepare_classifyunits/feature_units/__init__.py


# FEATUREUNIT-MANAGER
def get_featureunits(cu: object) -> None:
    """ Function to manage preprocessing steps as tokenization, normalization, stopwords removal, stemming and ngrams.
    Each step receives the current featureunits of a classifyunit-object and processes them. 
    Afterwards the new fus are set as featureunits for the cu (overwriting).
    
    Parameters
    ----------
    cu: object
        classifyunit-object which contains the instantiated featureunits --> consisting of cu-paragraphs without non-alphanumerical characters """

    # Tokenization
    fus = convert_featureunits.tokenize(cu.featureunits)
    cu.set_featureunits(fus)
    # Normalization
    fus = convert_featureunits.normalize(cu.featureunits, fus_config['normalize'])
    cu.set_featureunits(fus)
    # Stopwords Removal
    fus = convert_featureunits.filterSW(cu.featureunits, fus_config['filterSW'], Path(Configurations.get_stopwords_path()))
    cu.set_featureunits(fus)
    # Stemming
    fus = convert_featureunits.stem(cu.featureunits, fus_config['stem'])
    cu.set_featureunits(fus)
    # NGram Generation
    fus = convert_featureunits.gen_ngrams(cu.featureunits, fus_config['nGrams'], fus_config['continuousNGrams'])
    cu.set_featureunits(fus)
