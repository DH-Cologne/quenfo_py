"""Script to define Classes and Schemes for ORM-objects"""

# ## Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Float, Boolean, Column, Sequence, ForeignKey
from sqlalchemy.orm import backref, relationship
import itertools
import sklearn.neighbors
import sklearn.feature_extraction
import yaml
from pathlib import Path

# get Base connection
Base = declarative_base()

# ## Define Classes

# Class JobAds
class JobAds(Base):
    """ Checks and sets all JobAds values. Defines tablename, columnnames and makes values reachable. """
    # Tablename for matching with db table
    # TODO: declare in config
    __tablename__ = 'jobads'
    # Columns to query
    id = Column(Integer, Sequence('id'), primary_key=True)
    postingID = Column('postingID')
    jahrgang = Column('jahrgang')
    language = Column('language')
    content = Column('content')

    # JobAds have a parent-child relationship as a parent with ClassifyUnits.
    # ORM-relationship-type: One-to-many
    children = relationship("ClassifyUnits", back_populates="parent")

    # init-function to set values, works as constructor
    def __init__(self, id, posting_ID, jahrgang, language, content):
        self.id = id
        self.postingID = posting_ID
        self.jahrgang = jahrgang
        self.language = language
        self.content = content

    # Name the objects
    def __repr__(self):
        return "(%s, %s)" % (self.id, self.postingID)


# Class ClassifyUnits
class ClassifyUnits(Base):
    """ Checks and sets all ClassifyUnits values. Defines tablename, columnnames and makes values reachable. """
    # Tablename for matching with db table
    # TODO: declare in config
    __tablename__ = 'classify_units'
    # Columns to query
    id = Column(Integer, primary_key=True)
    classID = Column('classID', Integer)
    paragraph = Column('paragraph', String(225))
    # ClassifyUnits have a parent-child relationship as a child with JobAds.
    # ForeignKey to connect both Classes
    parent_id = Column(Integer, ForeignKey('jobads.id'))
    parent = relationship("JobAds", back_populates="children")
    # Set uid for each classify unit
    id_iter = itertools.count()
    # Set featureunit
    featureunits = list()
    # Set featurevector
    featurevectors = list()

    # init-function to set values, works as constructor
    def __init__(self, classID, paragraph, featureunits, featurevector):
        self.classID = classID
        self.paragraph = paragraph
        #self.id = next(ClassifyUnits.id_iter)
        self.featureunits = featureunits
        self.featurevector = featurevector

    # Name the objects
    def __repr__(self):
        return "(%s, %s)" % (self.id, self.parent.id)
    def set_featureunits(self, value):
        self.featureunits = value
    def set_featurevector(self, value):
        self.featurevector = value
    def set_classID(self, value):
        self.classID = value


# -------------------------------------------------------------------------------
# Class TrainingData
class TrainingData(Base):
    """ Checks and sets all TrainingData values. Defines tablename, columnnames and makes values reachable. """
    __tablename__ = 'traindata'
    index = Column(Integer, Sequence('index'), primary_key=True)
    postingId = Column('postingId', Integer)
    zeilennr = Column('zeilennr')
    classID = Column('classID')
    content = Column('content')
    children2 = relationship("ClassifyUnits_Train", back_populates="parent2")
    def __init__(self, postingId, zeilennr, classID, content):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content
    def __repr__(self):
        return "(%s, %s, %s)" % (self.postingId, self.zeilennr, self.classID)

# Class ClassifyUnits_Train
class ClassifyUnits_Train(Base):
    __tablename__ = 'classify_units_train'
    # Columns to query
    id = Column(Integer, primary_key=True)
    postingId = Column('postingId', Integer)
    zeilennr = Column('zeilennr', Integer)
    classID = Column('classID', Integer)
    content = Column('content', String)
    # ForeignKey to connect both Classes
    parent2 = relationship("TrainingData", back_populates="children2")
    parent_id2 = Column(Integer, ForeignKey('traindata.index'))
    # Set uid for each classify unit
    id_iter = itertools.count()
    # Set featureunit
    featureunits = list()
    # Set featurevector
    featurevectors = list()
    # init-function to set values, works as constructor
    def __init__(self, classID, content, featureunits, featurevector):
        self.classID = classID
        self.content = content
        self.id = next(ClassifyUnits.id_iter)
        self.featureunits = featureunits
        self.featurevector = featurevector
    # Name the objects
    def __repr__(self):
        return "(%s, %s)" % (self.id, self.parent2)
    # Setter
    def set_featureunits(self, value):
        self.featureunits = value
    def set_featurevector(self, value):
        self.featurevector = value
    def set_classID(self, value):
        self.classID = value

# ---------------------------------------------
# class Model which contains the knnclassifier and the tfidfvectorizer
class Model():
    # Set knn
    model_knn = sklearn.neighbors.KNeighborsClassifier()
    # Set vectorizer
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    # Set traindata information
    traindata_name = str()
    traindata_date = str()
    # init-function to set values, works as constructor
    def __init__(self, model_knn, vectorizer, traindata_name, traindata_date):
        self.model_knn = model_knn
        self.vectorizer = vectorizer
        self.traindata_name = traindata_name
        self.traindata_date = traindata_date

# class just to dump the traindatainfo with model
class TraindataInfo():
    def __init__(self, name, date):
        self.name = name
        self.date = date
    # Setter
    def set_name(self, value):
        self.name = value
    def set_date(self, value):
        self.date = value

# class just to dump model 
class SaveModel:
    def __init__(self, name):
        self.name = name

    def set_name(self, value):
        self.name = value

# Configuration Class
class Configurations():
    """ Class to get the parameters set in config.yaml and check if they are valid. 
        --> If not, set default values. """
        
    # ## Open Configuration-file and set variables + paths
    with open(Path('config.yaml'), 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
        models = cfg['models']
        fus_config = cfg['fus_config']
        query_limit = cfg['query_limit']
        mode = cfg['mode']
        tfidf_path = models['tfidf_path']
        knn_path = models['knn_path']
        tfidf_config = cfg['tfidf_config']
        knn_config = cfg['knn_config']
        resources = cfg['resources']
        traindata_path = resources['traindata_path']
        input_path = resources['input_path']
        stopwords_path = resources['stopwords_path']

    # Getter
    def get_traindata_path(): 
        traindata_path = Configurations.traindata_path
        return Configurations.__check_path(traindata_path)
    def get_tfidf_path(): 
        tfidf_path = Configurations.tfidf_path
        return Configurations.__check_path(tfidf_path)
    def get_knn_path(): 
        knn_path = Configurations.knn_path
        return Configurations.__check_path(knn_path)
    def get_input_path(): 
        input_path = Configurations.input_path
        return Configurations.__check_path(input_path)
    def get_stopwords_path(): 
        stopwords_path = Configurations.stopwords_path
        return Configurations.__check_path(stopwords_path)
    def get_query_limit():
        query_limit = Configurations.query_limit
        return Configurations.__check_type(query_limit, 50, int)
    def get_mode():
        mode = Configurations.mode
        return Configurations.__check_strings(mode, 'overwrite', ('append', 'overwrite'))
    def get_tfidf_config():
        tfidf_config = Configurations.tfidf_config
        if tfidf_config == None:
            tfidf_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        # give dictionary, key to check, defaultvalue if given value is wrong and type to check
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'lowercase', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'max_df', 1.0, float)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'min_df', 1, int)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'sublinear_tf', False, bool)
        tfidf_config = Configurations.__check_type_for_dict(tfidf_config, 'use_idf', True, bool)
        return tfidf_config
    def get_fus_config():
        fus_config = Configurations.fus_config
        if fus_config == None:
            fus_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        fus_config = Configurations.__check_type_for_dict(fus_config, 'normalize', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'stem', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'filterSW', True, bool)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'nGrams', {3,4}, dict)
        fus_config = Configurations.__check_type_for_dict(fus_config, 'continuousNGrams', False, bool)
        return fus_config
    def get_knn_config():
        knn_config = Configurations.knn_config
        if knn_config == None:
            knn_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        # give dictionary, key to check, defaultvalue if given value is wrong and type to check
        knn_config = Configurations.__check_type_for_dict(knn_config, 'n_neighbors', 5, int)
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'weights', 'uniform', ('uniform', 'distance'))
        knn_config = Configurations.__check_strings_for_dict(knn_config, 'algorithm', 'auto', ('auto', 'ball_tree', 'kd_tree', 'brute'))
        knn_config = Configurations.__check_type_for_dict(knn_config, 'leaf_size', 30, int)
        return knn_config
    
    # Checker + Default Setter
    def __check_path(path):
        try:
            Path(path).exists()
            path = path
        except FileNotFoundError:
            path = None
        return path

    def __check_type_for_dict(current_dict, key, default_val, type):
        try:
            if type(current_dict[key]) != type:
                raise KeyError
        except KeyError:
            try:
                current_dict[key] = default_val
            except KeyError:
                current_dict.update({key: default_val})
        return current_dict

    def __check_type(val_to_check, default_val, type):
        try:
            if type(val_to_check) != type:
                raise KeyError
        except KeyError:
            val_to_check = default_val
        return val_to_check

    def __check_strings(str_to_check, default_str, choices):
        try:
            if [s for s in choices if str(str_to_check) in s] == []:
                raise KeyError
        except KeyError:
            str_to_check = default_str
        return str_to_check

    def __check_strings_for_dict(current_dict, key, default_str, choices):
        str_to_check = current_dict[key]
        try:
            if [s for s in choices if str(str_to_check) in s] == []:
                raise KeyError
        except KeyError:
            try:
                current_dict[key] = default_str
            except KeyError:
                current_dict.update({key: default_str})
        return current_dict