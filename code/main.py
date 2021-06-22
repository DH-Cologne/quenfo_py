from ORM_structure import use_jobads
from ORM_structure import use_traindata
from ORM_structure import generate_output
from ORM_structure import manipulate_data
from database import session
from split_to_paragraph import jobads_to_paragraphs

print('test')
jobads = use_jobads()
#print(jobads)
print('beginner')
jobads_to_paragraphs(jobads)
session.commit()


""" # Load traindata and store it in list of objects
data = use_traindata()

for obj in data:
    # preprocess each obj
    print(obj)
    onestring = manipulate_data(obj)
    # write output
    generate_output(obj, onestring)

# commit sollte besser in orm.py aber dann wirds mehrmals aufgerufen deshalb erstmal hier.
session.commit() """
