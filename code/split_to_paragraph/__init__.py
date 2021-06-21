from . import splitter
from database import session
import sqlalchemy
from database import engine
from ORM_structure import orm
from ORM_structure.models import ClassifyUnits

# sowas wie wie main, kann vllt in init
def jobads_to_paragraphs(jobads: list):
    for jobad in jobads:
        print(jobad.id)
        #print(jobad.classify_units)
        list_paragraphs = splitter.split_at_empty_line(jobad)

        # add each paragraph in classify unit and write them in database
        for para in list_paragraphs:
            # Remove spaces at the beginning and at the end of the string
            para = splitter.remove_whitespaces(para)
            # Remove all non alpha-numerical characters
            para = splitter.replace(para)

            if para != '':
                child = ClassifyUnits(paragraph=para, classID=0)
                #über childen ist die classify unit mit der jobad verbunden (relationship parent -> child)
                jobad.children.append(child)
            
        #write in db
        orm.create_output(session, jobad)