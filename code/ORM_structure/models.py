from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Float, Boolean, Column, Sequence, ForeignKey
from sqlalchemy.orm import backref, relationship
from database import session
# ## TODO InputData Klasse erstellen (da fehlt die classID und Zeilennr)

Base = declarative_base()


class JobAds(Base):
    __tablename__ = 'jobads'
    id = Column(Integer, Sequence('id'), primary_key=True)
    postingID = Column('postingID')
    jahrgang = Column('jahrgang')
    language = Column('language')
    content = Column('content')
    #child_id = Column(Integer, ForeignKey('classify_units.id'))
    #classify_units = relationship("ClassifyUnits")
    children = relationship("ClassifyUnits", back_populates="parent")

    def __init__(self, id, posting_ID, jahrgang, language, content):
        self.id = id
        self.postingID = posting_ID
        self.jahrgang = jahrgang
        self.language = language
        self.content = content

    
    def __repr__(self):
        return "(%s, %s, %s, %s, %s)" % (self.id, self.postingID, self.jahrgang, self.language, self.content)

# Class classifyunit
class ClassifyUnits(Base):
    __tablename__ = 'classify_units'
    id = Column(Integer, primary_key=True)
    # neue felder
    classID = Column('classID', Integer)
    paragraph = Column('paragraph', String(225))
    # Declare relationship as child to parent (jobads)

    # Foreign key bezieht sich auf den table name!!! nicht auf ein attribute!!!
    #parent_id = Column(Integer, ForeignKey('JobAds.id'))
    #job_ads = relationship("JobAds", backref=backref("classify_units", lazy='noload'))

    parent_id = Column(Integer, ForeignKey('jobads.id'))
    parent = relationship("JobAds", back_populates="children")

    def __init__(self, classID, paragraph):
        self.classID = classID
        self.paragraph = paragraph

    def __repr__(self):
        return "(%s, %s)" % (self.classID, self.paragraph)






# fungiert letztlich als classifyunit (TODO umbenennen)
class TrainingData(Base):
    __tablename__ = 'traindata'
    index = Column(Integer, Sequence('index'), primary_key=True)
    postingId = Column('postingId')
    zeilennr = Column('zeilennr')
    classID = Column ('classID')
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
    classID = Column (Integer)
    content = Column(String(225))
    prepro = Column('prepro',String(225))

    def __init__(self, postingId, zeilennr, classID, content, prepro):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content
        self.prepro = prepro

    def __repr__(self):
        return "(%s, %s, %s, %s, %s)" % (self.postingId, self.zeilennr, self.classID, self.content, self.prepro)



