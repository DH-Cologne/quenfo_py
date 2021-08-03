"""Script to define Classes and Schemes for ORM-objects"""

# ## Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Float, Boolean, Column, Sequence, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.functions import array_agg
from database import session
import itertools

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
    def __init__(self, classID, paragraph, featureunits, featurevectors):
        self.classID = classID
        self.paragraph = paragraph
        self.id = next(ClassifyUnits.id_iter)
        self.featureunits = featureunits
        self.featurevectors = featurevectors

    # Name the objects
    def __repr__(self):
        return "(%s, %s)" % (self.id, self.parent.id)

    def set_featureunits(self, value):
        self.featureunits = value

    def set_featurevectors(self, value):
        self.featurevectors = value


# -------------------------------------------------------------------------------

class TrainingData(Base):
    __tablename__ = 'traindata'
    index = Column(Integer, Sequence('index'), primary_key=True)
    postingId = Column('postingId')
    zeilennr = Column('zeilennr')
    classID = Column('classID')
    content = Column('content')

    def __init__(self, postingId, zeilennr, classID, content):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content

    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.postingId, self.zeilennr, self.classID, self.content)


# Class OutputData
class OutputData(Base):
    __tablename__ = 'outputdata'
    index = Column(Integer, Sequence('index'), primary_key=True)
    postingId = Column(String(225))
    zeilennr = Column(Integer)
    classID = Column(Integer)
    content = Column(String(225))
    prepro = Column('prepro', String(225))

    def __init__(self, postingId, zeilennr, classID, content, prepro):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content
        self.prepro = prepro

    def __repr__(self):
        return "(%s, %s, %s, %s, %s)" % (self.postingId, self.zeilennr, self.classID, self.content, self.prepro)
