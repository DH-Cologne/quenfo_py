from sklearn.neighbors import KNeighborsClassifier 
import training 
import yaml
from pathlib import Path

# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
     cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
     config = cfg['knn_config']

def initialize_knn(tfidf_train, all_classes):

     # knn prototyp
     knn = KNeighborsClassifier(n_neighbors=config['n_neighbors'], weights=config['weights'], \
          algorithm=config['algorithm'], leaf_size=config['leaf_size'], metric=config['metric'])
     clf = knn.fit(tfidf_train, all_classes)

     # save the model
     training.save_model(clf)
     return clf