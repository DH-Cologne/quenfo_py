from numpy import array
from sklearn.feature_extraction.text import CountVectorizer
is_created = None
bow_train = [[]]


def initialize_bow_train(traindata):

    global is_created
    global bow_train
    all_features = list()
    
    if is_created is None:
        traindata
        for train_obj in traindata:
            for cu in train_obj.children2:
                all_features.append(cu.featureunits)
                """ for fu in cu.featureunits:
                    all_features.append(fu) """
        bow_train = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform(all_features).toarray()
        is_created = 'checked'
        return bow_train
    else:
        return bow_train


def gen_bow_cu(fus):
    # TODO: NACHSEHEN OB DIE FEATURES HIER WIrklich die featureuntis zsm geschmissen werden sollen (wahrschienlich ja aber überprüfen)
    bow_cu = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform(fus).toarray()
    return bow_cu
    