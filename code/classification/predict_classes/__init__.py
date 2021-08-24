from . import knn_predictor

def start_prediction(jobad, model):

    for cu in jobad.children:

        predicted = knn_predictor.gen_classes(cu.featurevector, model.model_knn)
        # hier dann auch den regex predictor reinmachen und dann direkt vergleichen!
        
        cu.set_classID(predicted[0].replace('\n', ''))
        print(cu, predicted[0].replace('\n', ''))
