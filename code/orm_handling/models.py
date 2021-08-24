"""Script to define Classes and Schemes for ORM-objects"""

# ## Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Float, Boolean, Column, Sequence, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.util.langhelpers import NoneType
from database import session
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


class Configurations():

    # ## Open Configuration-file and set variables + paths
    with open(Path('config.yaml'), 'r') as yamlfile:
        cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
        models = cfg['models']
        tfidf_path = models['tfidf_path']
        knn_path = models['knn_path']
        tfidf_config = cfg['tfidf_config']
        knn_config = cfg['knn_config']
        resources = cfg['resources']
        traindata_path = resources['traindata_path']


    # Getter
    def get_traindata_path(): 
        traindata_path = Configurations.traindata_path
        try:
            Path(traindata_path).exists()
            traindata_path = traindata_path
        except FileNotFoundError:
            traindata_path = None
        return traindata_path

    def get_tfidf_path(): 
        tfidf_path = Configurations.tfidf_path
        try: 
            Path(tfidf_path).exists()
            tfidf_path = tfidf_path
        except FileNotFoundError:
            tfidf_path = None
        return tfidf_path

    def get_knn_path(): 
        knn_path = Configurations.knn_path
        try: 
            Path(knn_path).exists()
            knn_path = knn_path
        except FileNotFoundError:
            knn_path = None
        return knn_path


    def get_tfidf_config():

        tfidf_config = Configurations.tfidf_config
        
        if type(tfidf_config['lowercase']) == bool:
            pass
        else:
            tfidf_config['lowercase'] = False
        if type(tfidf_config['max_df']) == float:
            pass
        else:
            tfidf_config['max_df'] = 1.0
        if type(tfidf_config['min_df']) == int:
            pass
        else:
            tfidf_config['min_df'] = 1
        if type(tfidf_config['sublinear_tf']) == bool:
            pass
        else:
            tfidf_config['sublinear_tf'] = False
        if type(tfidf_config['use_idf']) == bool:
            pass
        else:
            tfidf_config['use_idf'] = True

        return tfidf_config

    def get_knn_config():
        knn_config = Configurations.knn_config
        if knn_config == None:
            knn_config = dict()
        # with these Exceptions, missing and wrong input is fixed and also if all knn data is missing
        try:
            if type(knn_config['n_neighbors']) != int:
                raise KeyError
        except KeyError:
            try:
                knn_config['n_neighbors'] = 5
            except KeyError:
                knn_config.update({'n_neighbors': 5})
        try:
            if (knn_config['weights']) != 'uniform' or (knn_config['weights']) != 'distance':
                raise KeyError
        except KeyError:
            try:
                knn_config['weights'] = 'uniform'
            except KeyError:
                knn_config.update({'weights': 'uniform'})
        try:
            a = knn_config['algorithm']
            if a != 'auto' or a != 'ball_tree' or a != 'kd_tree' or a != 'brute':
                raise KeyError
        except KeyError:
            try:
                knn_config['algorithm'] = 'auto'
            except KeyError:
                knn_config.update({'algorithm': 'auto'})
        try:
            if type(knn_config['leaf_size']) != int:
                raise KeyError
        except KeyError:
            try:
                knn_config['leaf_size'] = 30
            except KeyError:
                knn_config.update({'leaf_size': 30})
        
        return knn_config

    

""" class Configurations():

    def __init__(self):
        # ## Open Configuration-file and set variables + paths
        with open(Path('config.yaml'), 'r') as yamlfile:
            cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
            models = cfg['models']
            tfidf_path = models['tfidf_path']
            knn_path = models['knn_path']
            tfidf_config = cfg['tfidf_config']
            knn_config = cfg['knn_config']
            resources = cfg['resources']
            traindata_path = resources['traindata_path']

        self.tfidf_path = tfidf_path
        self.knn_path = knn_path
        self.tfidf_config = tfidf_config
        self.knn_config = knn_config
        self.traindata_path = traindata_path

    # Getter
    def get_traindata_path(self): 
        return self.traindata_path

    def get_tfidf_path(self): 
        return self.tfidf_path
    def get_knn_path(self): 
        return self.knn_path

    # Setter-Checker
    def set_tfidf_path(self):
        tfidf_path = self.tfidf_path
        try: 
            Path(tfidf_path).exists()
            self.tfidf_path = tfidf_path
        except FileNotFoundError:
            self.tfidf_path = None
    def set_knn_path(self):
        knn_path = self.knn_path
        try: 
            Path(knn_path).exists()
            self.tfidf_path = knn_path
        except FileNotFoundError:
            self.knn_path = None

    def set_traindata_path(self):
        traindata_path = self.traindata_path
        try:
            Path(traindata_path).exists()
            self.traindata_path = "../test.db"
        except FileNotFoundError:
            self.traindata_path = None

    def set_tfidf_config(self):
        tfidf_config = self.tfidf_config
        print(tfidf_config)
        lowercase: False
        max_df: 1.0 
        min_df: 1
        sublinear_tf: False
        use_idf: True
        if type(tfidf_config['lowercase']) == bool:
            self.tfidf_config ==
        else:
            self.full_param = True """


