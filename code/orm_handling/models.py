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


""" class ExtractionUnits(Base):
    #Checks and sets all ExtractionUnits values. Defines tablename, columnnames and makes values reachable.

    # Tablename for matching with db table
    # TODO: declare in config
    __tablename__ = 'extraction_units'
    # Columns to query
    id = Column(Integer, primary_key=True)
    paragraph = Column('paragraph', ClassifyUnits)
    position_index = Column('position_index', int)
    sentence = Column('sentence', String(225))
    # TODO type for token_array, in java: Texttoken
    token_array = Column("token_array")

    # ExtractionUnits have a parent-child relationship as a child with ClassifyUnits.
    # ForeignKey to connect both Classes
    parent_id = Column(Integer, ForeignKey('classify_units.id'))
    parent = relationship('ClassifyUnits', back_populates="children")

    # Set lexical data
    token = list()
    lemmata = list()
    pos_tags = list()

    # init-function to set values, works as constructor
    def __init__(self, paragraph, position_index, sentence, token_array, token, lemmata, pos_tags):
        self.paragraph = paragraph
        self.position_index = position_index
        self.sentence = sentence
        self.token_array = token_array
        self.token = token
        self.lemmata = lemmata
        self.pos_tags = pos_tags

    def set_lexicaldata(self, token, lemmata, pos_tags):
        self.token = token
        self.lemmata = lemmata
        self.pos_tags = pos_tags """


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
