from sqlalchemy.sql.expression import false
from ORM_structure import objects
from ORM_structure import orm
from database import session
from ORM_structure import preprocessing

data = list
print('in orm init')

def use_jobads() -> list:
    jobads = orm.get_jobads(session)
    return jobads
    
# ## Input
def use_traindata():
    data = orm.get_traindata(session)
    return data







"""Hier passiert was mit data und die daten werden vorverarbeitet/manipuliert und die veränderten Daten/Analysedaten werden dann an generate_output weitergegeben
Der nimmt sich dann was er braucht, um es in die Output db zu packen"""

def manipulate_data(obj):
    
    onestring = preprocessing.prepro(obj)
        
    return onestring


# ## Output
def generate_output(obj, onestring):
 
    output_obj = objects.create_output_object(obj, onestring)
    orm.create_output(session, output_obj)
    


