from sklearn.feature_extraction.text import TfidfVectorizer
import training
import yaml
from pathlib import Path

## TODO: Setter einbauen für default einstellungen

# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
     cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
     config = cfg['tfidf_config']


def initialize_vectorizer(all_features):

    vectorizer = TfidfVectorizer(lowercase=config['lowercase'], max_df=config['max_df'], \
        min_df=config['min_df'], sublinear_tf=config['sublinear_tf'], use_idf=config['use_idf']).fit(all_features)

    tfidf_train = vectorizer.transform(all_features)

    # save the model
    training.save_model(vectorizer)


    return vectorizer, tfidf_train

    


