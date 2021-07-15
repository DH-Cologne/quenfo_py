from . import convert_featureunits
import yaml
from pathlib import Path

# ## Open Configuration-file and set paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    fus_config = cfg['fus_config']
    resources = cfg['resources']

def get_featureunits(cu: object) -> str:
    fus = convert_featureunits.tokenize(cu.featureunits)
    cu.set_featureunits(fus)
    fus = convert_featureunits.normalize(cu.featureunits, fus_config['normalize'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.filterSW(cu.featureunits, fus_config['filterSW'], Path(resources['stopwords_path']))
    cu.set_featureunits(fus)
    fus = convert_featureunits.stem(cu.featureunits, fus_config['stem'])
    cu.set_featureunits(fus)
    fus = convert_featureunits.gen_ngrams(cu.featureunits, fus_config['nGrams'], fus_config['continousNGrams'])
    cu.set_featureunits(fus)