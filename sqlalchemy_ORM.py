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
for class_instance in data:
    print(vars(class_instance))
    print(class_instance.zeilennr)
    print(class_instance.content)


session.close()