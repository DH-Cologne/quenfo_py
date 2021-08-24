from orm_handling.models import Configurations
from sklearn.feature_extraction.text import TfidfVectorizer
import training


config = Configurations.get_tfidf_config()


def initialize_vectorizer(all_features):

    vectorizer = TfidfVectorizer(lowercase=config['lowercase'], max_df=config['max_df'], \
        min_df=config['min_df'], sublinear_tf=config['sublinear_tf'], use_idf=config['use_idf']).fit(all_features)

    tfidf_train = vectorizer.transform(all_features)

    # save the model
    training.save_model(vectorizer)


    return vectorizer, tfidf_train

    


