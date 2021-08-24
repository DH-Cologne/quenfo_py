from orm_handling.models import Configurations
from sklearn.neighbors import KNeighborsClassifier 
import training 


config = Configurations.get_knn_config()

def initialize_knn(tfidf_train, all_classes):

     # knn prototyp
     knn = KNeighborsClassifier(n_neighbors=config['n_neighbors'], weights=config['weights'], \
          algorithm=config['algorithm'], leaf_size=config['leaf_size'])
     clf = knn.fit(tfidf_train, all_classes)

     # save the model
     training.save_model(clf)
     return clf