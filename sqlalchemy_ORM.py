from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Sequence
from sqlalchemy import String, Integer, Float, Boolean, Column
from sqlalchemy.orm import sessionmaker
import os

input_path = os.path.join('..', 'traindata_sql.db')

Base = declarative_base()

class MyTable(Base):
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


engine = create_engine('sqlite:///' + input_path, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(MyTable).all()
# Printet alle sqlalchemy.orm.state.InstanceState objects (alle row einträge in der database die im ORM gestored sind)
""" The SQLAlchemy ORM will return an instance of a class by default (erste print) """
for class_instance in data:
    """ The SQLAlchemy ORM will return an instance of a class by default (erste print) """
    print(class_instance)
    # kann sich die objekte als vars ausgeben lassen
    print(vars(class_instance))
    # einzelne features der objekte printen
    print(class_instance.zeilennr)
    print(class_instance.content)
    # objekte als dicts printen == If you're looking to get dictionaries instead, use the built-in __dict__ method:
    print(class_instance.__dict__)

    # oder als eigenes Objekt (etwas gedoppelt dadurch)
    dataObject = {
        'postingID': class_instance.postingId,
        'zeilennr': class_instance.zeilennr,
        'classID': class_instance.classID,
        'content': class_instance.content
    }
    print(dataObject)


session.close()

# Ausprobieren: 
# Daten verändern und wieder in neue table schreiben
# blobs erzeugen 
# Daten bei mehreren Tables verwalten? (iterieren über Datenbank)
# Schemata genauer ansehen 