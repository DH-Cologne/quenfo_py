# ## Imports
from orm_handling.models import Configurations
from . import convert_featureunits
from pathlib import Path

fus_config = Configurations.get_fus_config()


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
