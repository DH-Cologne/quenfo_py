""" Script to define Classes and Schemes for ORM-objects
    Classes:
        a. JobAds               --> JobAds to be splitted and classified
        b. ClassifyUnits        --> preprocessed and classified paragraphs
        c. TrainData            --> Traindata (already in paragraphs and classified)
        d. ClassifyUnits_Train  --> contains each Traindata paragraph (preprocessed and classified)
        e. ExtrationUnits       --> preprocessed and splitted sentences from paragraphs
        f. InformationEntity    --> extracted entities"""

# ## Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, Sequence, PickleType, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import itertools
from sqlalchemy.ext.mutable import MutableList

# get Base connection
Base = declarative_base()

# ## Define Classes

# *** JOBADS/CU MODELS ***


# Class JobAds
class JobAds(Base):
    """ Checks and sets all JobAds values. Defines tablename, columnnames and makes values reachable. """
    __tablename__ = 'jobads'                                            # Tablename for matching with db table
    id = Column(Integer, Sequence('id'), primary_key=True)              # Columns to query
    postingID = Column('postingID')
    jahrgang = Column('jahrgang')
    language = Column('language')
    content = Column('content')

    # JobAds have a parent-child relationship as a parent with ClassifyUnits.
    children = relationship("ClassifyUnits", back_populates="parent")   # ORM-relationship-type: One-to-many

    # init-function to set values
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
    __tablename__ = 'classify_units'                                    # Tablename for matching with db table
    id = Column(Integer, primary_key=True)                              # Columns to query
    classID = Column('classID', Integer)
    paragraph = Column('paragraph', String(225))
    parent_id = Column(Integer, ForeignKey('jobads.id'))                # ClassifyUnits have a parent-child relationship as a child with JobAds.
    parent = relationship("JobAds", back_populates="children")          # ForeignKey to connect both Classes
    children = relationship("ExtractionUnits", back_populates="parent") # Each CU is parent of ExtractionUnits
    id_iter = itertools.count()                                         # Set uid for each classify unit
    featureunits = list()                                               # Set featureunit
    featurevectors = list()                                             # Set featurevector

    # init-function to set values
    def __init__(self, classID, paragraph, featureunits, featurevector):
        self.classID = classID
        self.paragraph = paragraph
        self.featureunits = featureunits
        self.featurevector = featurevector

    # Name the objects
    def __repr__(self):
        return "(%s, %s)" % (self.id, self.parent.id)

    # Setter
    def set_featureunits(self, value):
        self.featureunits = value

    def set_featurevector(self, value):
        self.featurevector = value

    def set_classID(self, value):
        self.classID = value


# *** TRAINDATA MODELS ***

# Class TrainingData
class TrainingData(Base):
    """ Checks and sets all TrainingData values. Defines tablename, columnnames and makes values reachable. """
    __tablename__ = 'traindata'                                                 # Tablename for matching with db table
    index = Column(Integer, Sequence('index'), primary_key=True)                # Columns to query
    postingId = Column('postingId', Integer)
    zeilennr = Column('zeilennr')
    classID = Column('classID')
    content = Column('content')
    children2 = relationship("ClassifyUnits_Train", back_populates="parent2")   # parent-child relationship as a parent

    # init-function to set values
    def __init__(self, postingId, zeilennr, classID, content):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content

    # Name the objects
    def __repr__(self):
        return "(%s, %s, %s)" % (self.postingId, self.zeilennr, self.classID)


# Class ClassifyUnits_Train
class ClassifyUnits_Train(Base):
    """ Checks and sets all ClassifyUnits_Train values. Defines tablename, columnnames and makes values reachable. """
    __tablename__ = 'classify_units_train'                                      # Tablename for matching with db table
    id = Column(Integer, primary_key=True)                                      # Columns to query
    postingId = Column('postingId', Integer)
    zeilennr = Column('zeilennr', Integer)
    classID = Column('classID', Integer)
    content = Column('content', String)
    parent2 = relationship("TrainingData", back_populates="children2")          # parent-child relationship as a child
    parent_id2 = Column(Integer, ForeignKey('traindata.index'))                 # ForeignKey to connect both Classes
    featureunits = list()                                                       # Set featureunit
    featurevectors = list()                                                     # Set featurevector

    # init-function to set values, works as constructor
    def __init__(self, classID, content, featureunits, featurevector):
        self.classID = classID
        self.content = content
        self.featureunits = featureunits
        self.featurevector = featurevector

    # Name the objects
    def __repr__(self):
        return "(%s%s)" % (self.id, self.parent2)

    # Setter
    def set_featureunits(self, value):
        self.featureunits = value

    def set_featurevector(self, value):
        self.featurevector = value

    def set_classID(self, value):
        self.classID = value


class ExtractionUnits(Base):
    """ Checks and sets all ExtractionUnits values. Defines tablename, columnnames and makes values reachable. """
    parent_id = Column(Integer, ForeignKey('classify_units.id'))                # ExtractionUnits have a parent-child relationship as a child with ClassifyUnits.
    parent = relationship('ClassifyUnits', back_populates="children")           # ForeignKey to connect both Classes
    children = relationship("InformationEntity", back_populates="parent")       # parent-child relationship as a parent
    __tablename__ = 'extraction_units'                                          # Tablename for matching with db table
    id = Column(Integer, primary_key=True)                                      # Columns to query
    paragraph = Column('paragraph', String(225))
    position_index = Column('position_index', Integer)
    sentence = Column('sentence', String(225))
    token_array = Column("token_array", MutableList.as_mutable(PickleType), default=[])

    # Set lexical data
    token = list()
    lemmata = list()
    pos_tags = list()

    # init-function to set values
    def __init__(self, paragraph, position_index, sentence, token_array, token, lemmata, pos_tags):
        self.paragraph = paragraph
        self.position_index = position_index
        self.sentence = sentence
        self.token_array = token_array
        self.token = token
        self.lemmata = lemmata
        self.pos_tags = pos_tags


class InformationEntity(Base):
    """ Checks and sets all InformationEntity values. Defines tablename, columnnames and makes values reachable. """
    parent_id = Column(Integer, ForeignKey('extraction_units.id'))              # InformationEntity have a parent-child relationship as a child with ExtractionUnits.
    parent = relationship('ExtractionUnits', back_populates="children")         # ForeignKey to connect both Classes
    __tablename__ = 'extracted_entities'                                        # Tablename for matching with db table
    id = Column(Integer, primary_key=True)                                      # Columns to query
    sentence = Column('extraction_unit', String(225))                           # extraction_unit with found entity
    ie_type = Column("ie_type", String(225))                                    # type
    start_lemma = Column("start_lemma", String(225))                            # start_lemma: first string
    is_single_word = Column("is_single_word", Boolean)                          # single word entity?
    full_expression = Column("full_expression", String(225))                    # multi word entity -> full expression as string
    lemma_array = Column("lemma_array", MutableList.as_mutable(PickleType), default=[])
    modifier = Column("modifier", String(225))                                  # used modifier
    first_index = int

    # init-function to set values
    def __init__(self, ie_type, start_lemma, is_single_word):
        self.ie_type = ie_type
        self.start_lemma = start_lemma
        self.is_single_word = is_single_word

    # Setter
    def set_sentence(self, sentence: str):
        self.sentence = sentence

    def set_full_expression(self, full_expression: str):
        self.full_expression = full_expression

    def set_lemma_array(self, lemma_array: list):
        self.lemma_array = lemma_array

    def set_modifier(self, modifier: str):
        self.modifier = modifier

    def set_first_index(self, first_index: int):
        self.first_index = first_index

