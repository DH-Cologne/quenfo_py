# ## Imports
from ORM_structure import orm
from database import session

# TODO: Kommentare hier irgendwie unnötig. Vllt kann diese init auch leer bleiben.

# Initiate session 
# and pass it function get_jobads in module orm to read db-table and store rows as objects

""" def use_jobads() -> list: """
""" Function manages the initiation of a session, loading of input-data and handling data as orm-objects

Returns
-------
jobads: list
    Data contains the orm-objects from class JobAds """

""" jobads = orm.get_jobads(session)
return jobads """







# ---------------------------------------------------
    
""" # ## Input
def use_traindata():
    data = orm.get_traindata(session)
    return data """


"""Hier passiert was mit data und die daten werden vorverarbeitet/manipuliert und die veränderten Daten/Analysedaten werden dann an generate_output weitergegeben
Der nimmt sich dann was er braucht, um es in die Output db zu packen"""

""" def manipulate_data(obj):
    
    onestring = preprocessing.prepro(obj)
        
    return onestring


# ## Output
def generate_output(obj, onestring):
 
    output_obj = objects.create_output_object(obj, onestring)
    orm.create_output(session, output_obj) """
    


