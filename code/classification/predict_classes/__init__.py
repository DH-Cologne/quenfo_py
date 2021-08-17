from . import knn_predictor
def start_prediction(jobad, model):

    for cu in jobad.children:

        clf = model.model_knn
        predicted = knn_predictor.gen_classes(cu.featurevector, clf)
        cu.set_classID(predicted[0].replace('\n', ''))
        print(cu, predicted[0].replace('\n', ''))
