from sklearn.feature_extraction.text import TfidfVectorizer
import training


tfidf_train = ''
vectorizer =''



def initialize_vectorizer(all_features, traindata_namedate):

    global tfidf_train
    global vectorizer


    vectorizer = TfidfVectorizer(lowercase=False, input=traindata_namedate).fit(all_features)
    tfidf_train = vectorizer.transform(all_features)

    # save the model
    training.save_model(vectorizer)


    return vectorizer, tfidf_train

    


