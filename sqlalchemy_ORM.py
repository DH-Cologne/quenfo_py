from typing import Text
from numpy import string_
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Sequence
from sqlalchemy import String, Integer, Float, Boolean, Column
from sqlalchemy.orm import sessionmaker
import os
import os, psutil
import sqlite3
from sqlite3 import Error
import pandas as pd
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

""" Gerade sind hier zwei Herangehensweisen drinnen, um die Daten (Trainingsdaten) einzulesen. Einmal mittels Sqlalchemy ORM Objects und einmal über sqlite3 Anfragen und Verwaltung in DF/Dicts
Beide haben bezügl. des memory usages ähnliche Kapazitäten. Die Klassenstruktur mittels ORM bietet aber einheitlichere Verwaltungsstrukturen. """

# wie viel memory wird belegt?
process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes 

input_path = os.path.join('..', 'traindata_sql.db')


Base = declarative_base()

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


engine = create_engine('sqlite:///' + input_path, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# data enthält alle Objekte der Klasse myClass die row-wise gefüllt wurden --> data ist eine liste
data = session.query(TrainingData).all()

# Printet alle sqlalchemy.orm.state.InstanceState objects (alle row einträge in der database die im ORM gestored sind)

""" The SQLAlchemy ORM will return an instance of a class by default (erste print) """
for class_instance in data:
    """ The SQLAlchemy ORM will return an instance of a class by default (erste print) """
    #print(class_instance)
    # kann sich die objekte als vars ausgeben lassen
    print(vars(class_instance))
    # einzelne features der objekte printen
    print(class_instance.zeilennr)
    #print(class_instance.content)
    # objekte als dicts printen == If you're looking to get dictionaries instead, use the built-in __dict__ method:
    #print(class_instance.__dict__)


    # oder als eigenes Objekt (etwas gedoppelt dadurch) und deserialisiert!
    dataObject = {
        'postingID': class_instance.postingId,
        'zeilennr': class_instance.zeilennr,
        'classID': class_instance.classID,
        'content': class_instance.content
    }
    """ print(dataObject) """

session.close()

#meta = MetaData()

# Class OutputData
class OutputData(Base):
    __tablename__ = 'outputdata'
    index = Column(Integer, Sequence('index'), primary_key=True)
    postingId = Column(String(225))
    zeilennr = Column(Integer)
    classID = Column (Integer)
    content = Column(String(225))

    def __init__(self, postingId, zeilennr, classID, content):
        self.postingId = postingId
        self.zeilennr = zeilennr
        self.classID = classID
        self.content = content

engine = create_engine('sqlite:///' + input_path, echo=True)
#Base.metadata.tables['outputdata'].create(engine)
try:
    OutputData.__table__.create(engine)
except sqlalchemy.exc.OperationalError:
    print("table does already exist")
    pass

#Base.metadata.create_all(engine)
#engine = create_engine('sqlite:///' + input_path, echo=True)
#outdata = session.query(OutputData).all()
#meta.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

for class_instance in data:
    output = OutputData(

        postingId=class_instance.postingId,
        zeilennr=class_instance.zeilennr,
        classID=class_instance.classID,
        content=class_instance.content
    )

    

    #Base.metadata.tables["outputdata"].create(bind = engine)
    session.add(output)
session.commit()


# wie viel memory wird belegt?
process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes 

# Ausprobieren: 
# Daten verändern und wieder in neue table schreiben (Objects generieren und der DB hinzufügen)
# blobs erzeugen 
# Daten bei mehreren Tables verwalten? (iterieren über Datenbank)
# Schemata genauer ansehen 




##################################################################################
"""!!!!!!!!!!!!!!! Vergleich mit Einlesen der Daten in df und dict bestehend aus df --> Vergleich des memory-usage"""
def conn_testing():
    database = input_path
    #database = os.path.join('temp', 'final_testset.db')
    print(database)
    # create a database connection
    try:
        conn_temp = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn_temp

def get_df_id(conn):

    print("id section")
    ### try dataframe
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    counter = 0
    frames = {}
    for name in res:
        if "tx_2019_12" in name[0] or "tx_2019_11" in name[0]:
            df_temp = pd.DataFrame()
            print(name[0])
            chunk_size = 2500
            df_store = pd.read_sql(("SELECT * FROM {}".format(name[0])), conn, chunksize = chunk_size)
            #print(len(df_store))
            #for row in df_store.iteritems(): 
            for chunk in df_store: 
                counter+=chunk_size
                print(counter)
                if counter == 2500 or len(chunk) < chunk_size:
                    df_temp = df_temp.append(chunk)
                    df_temp = df_temp.reset_index(drop=True)
                    df_temp['index'] = df_temp.index
                    frames[name[0]] = df_temp
                    counter=0
                    break
                else: 
                    df_temp = df_temp.append(chunk)
                    pass
        else:
            continue
    df = frames 

    #print(df)


conn=conn_testing()
get_df_id(conn)

process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes 