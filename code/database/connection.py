from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import os


input_path = os.path.join('..','..', 'traindata_sql.db')

engine = create_engine('sqlite:///' + input_path, echo=False)

Session = sessionmaker(bind=engine)
session = Session()