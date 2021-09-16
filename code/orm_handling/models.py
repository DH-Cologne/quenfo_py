"""Script to define Classes and Schemes for ORM-objects"""

# ## Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, Sequence, ForeignKey, PickleType, Boolean
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import backref, relationship
import itertools
import sklearn.neighbors
import sklearn.feature_extraction

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


class ExtractionUnits(Base):
    """ Checks and sets all ExtractionUnits values. Defines tablename, columnnames and makes values reachable. """
    # ExtractionUnits have a parent-child relationship as a child with ClassifyUnits.
    # ForeignKey to connect both Classes
    parent_id = Column(Integer, ForeignKey('classify_units.id'))
    parent = relationship('ClassifyUnits', back_populates="children")
    children = relationship("InformationEntity", back_populates="parent")

    # Tablename for matching with db table
    # TODO: declare in config
    __tablename__ = 'extraction_units'

    # Columns to query
    id = Column(Integer, primary_key=True)
    paragraph = Column('paragraph', String(225))
    position_index = Column('position_index', Integer)
    sentence = Column('sentence', String(225))
    # TODO type for token_array, in java: Texttoken
    # try pickle? token_array = list[Token]
    token_array = Column("token_array", MutableList.as_mutable(PickleType), default=[])

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


class InformationEntity(Base):
    """ Checks and sets all InformationEntity values. Defines tablename, columnnames and makes values reachable. """
    # InformationEntity have a parent-child relationship as a child with ExtractionUnits.
    # ForeignKey to connect both Classes
    parent_id = Column(Integer, ForeignKey('extraction_units.id'))
    parent = relationship('ExtractionUnits', back_populates="children")

    # Tablename for matching with db table
    # TODO: declare in config
    __tablename__ = 'extracted_entities'

    # Columns to query
    id = Column(Integer, primary_key=True)
    # extraction_unit with found entity
    sentence = Column('extraction_unit', String(225))
    # matched pattern description
    pattern = Column('pattern_string', String(225))
    # type
    ie_type = Column("ie_type", String(225))
    # start_lemma: first string
    start_lemma = Column("start_lemma", String(225))
    # single word entity?
    is_single_word = Column("is_single_word", Boolean)
    # multi word entity -> full expression as string
    full_expression = Column("full_expression", String(225))
    # save as BLOB -> pickle?
    # multi word entity -> full expression as array
    lemma_array = Column("lemma_array", MutableList.as_mutable(PickleType), default=[])
    # used modifier
    modifier = Column("modifier", String(225))

    first_index = int

    def __init__(self, sentence, pattern, ie_type, start_lemma, is_single_word, full_expression, lemma_array, modifier,
                 first_index):
        self.sentence = sentence
        self.pattern = pattern
        self.ie_type = ie_type
        self.start_lemma = start_lemma
        self.is_single_word = is_single_word
        self.full_expression = full_expression
        self.lemma_array = lemma_array
        self.modifier = modifier
        self.first_index = first_index
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
