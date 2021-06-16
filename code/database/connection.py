"""Create SQLAlchemy engine and session objects."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from ORM_structure import objects
import sqlalchemy
import os


input_path = os.path.join('..','..', 'traindata_sql.db')

engine = create_engine('sqlite:///' + input_path, echo=True)

Session = sessionmaker(bind=engine)
session = Session()