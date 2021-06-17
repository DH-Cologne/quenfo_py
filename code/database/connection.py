from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import os


#input_path = os.path.join('..','..', 'traindata_sql.db')
input_path = os.path.join('..','..', 'text_kernel_orm_2018_03.db')

engine = create_engine('sqlite:///' + input_path, echo=False)
print(input_path)
Session = sessionmaker(bind=engine)
session = Session()