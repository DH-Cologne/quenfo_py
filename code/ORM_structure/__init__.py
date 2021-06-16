from sqlalchemy.sql.expression import false
from ORM_structure import objects
from ORM_structure import orm
from database import session

data = list

def use_traindata():
    data = orm.get_traindata(session)
    return data

"""Hier passiert was mit data und die daten werden vorverarbeitet/manipuliert und die veränderten Daten/Analysedaten werden dann an generate_output weitergegeben
Der nimmt sich dann was er braucht, um es in die Output db zu packen"""

def generate_output(data):
    for obj in data:
        output_obj = objects.create_output_object(obj)
        orm.create_output(session, output_obj)
    # commit sollte besser in orm.py aber dann wirds mehrmals aufgerufen deshalb erstmal hier.
    session.commit()


def convert_data():
    traindata = use_traindata()
    generate_output(traindata)
