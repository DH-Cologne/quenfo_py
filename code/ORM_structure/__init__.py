from ORM_structure import objects
from ORM_structure import orm
""" from ORM_structure import orm
from ORM_structure import objects """
from database import session

def generate_output():
    # Create admin user & two posts
    output_obj = objects.create_output_object()
    print(output_obj)
    orm.create_output(session, output_obj)

