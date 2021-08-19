"""Script to build data and to create data"""

# ## Imports
from database.connection import Session2
from sqlalchemy.orm import Session, query, session
from .models import ClassifyUnits, ClassifyUnits_Train, TrainingData, JobAds
import sqlalchemy
from database import engine, engine2
import yaml
from pathlib import Path

# ## Variables
is_created = None


# ## Open Configuration-file and set variables + paths
with open(Path('config.yaml'), 'r') as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    query_limit = cfg['query_limit']
    mode = cfg['mode']


# Function to query the data from the db table
def get_jobads(session: Session) -> list:
    """ Function manages the data query and instantiates the Schema for the class JobAds in models.py

    Parameters
    ----------
    session: Session
        Session object, generated in module database. Contains the database path

    Returns
    -------
    jobads: list
        Data contains the orm-objects from class JobAds 
    
    Raises
    ------
    sqlalchemy.exc.OperationalError
        If changes in db are not possible, OperationalError is raised to continue with creation of table """

    # load the jobads
    job_ads = session.query(JobAds).limit(query_limit).all()

    try:
        # delete the handles from jobads to classifunits or create new table
        if mode == "overwrite":
            session.query(ClassifyUnits).delete()
        # load all related classify units for appending
        else:
            session.query(ClassifyUnits).filter(ClassifyUnits.parent_id == JobAds.id).all()

    except sqlalchemy.exc.OperationalError:
        print("table classify_unit not existing --> create new one")
        ClassifyUnits.__table__.create(engine)

    pass_output(session)
    
    return job_ads


def get_traindata(session2: Session) -> list:
    """ Function manages the data query and instantiates the Schema for the class TrainingData in models.py

    Parameters
    ----------
    session2: Session
        Session object, generated in module database. Contains the database path

    Returns
    -------
    traindata: list
        Data contains the orm-objects from class TrainingData """

    # load the TrainingData
    traindata = session2.query(TrainingData).all()
    
    try:
        ClassifyUnits_Train.__table__.create(engine2)
    except sqlalchemy.exc.OperationalError:
        print("table does already exist")
        ClassifyUnits_Train.__table__.drop(engine2)
        ClassifyUnits_Train.__table__.create(engine2)
        pass

    # return Trainindata objects as list
    return traindata

def delete_filler(session2):
    # remove all unwanted in memory stored objects and just drp the table in traindata
    session2.rollback()
    ClassifyUnits_Train.__table__.drop(engine2)

def pass_output(session: Session):
    """ The session.commit() statement commits all adds to the current session.

    Parameters
    ----------
    session: Session
        Session object, generated in module database. Contains the database path. """

    session.commit()


# Function to manage session adding
def create_output(session: Session, output: object):
    """ Function checks if table to store output in already exists. Else the table is dropped and created again.
    The session.add(object) statement adds the passed object to the current session.

    Parameters
    ----------
    session: Session
        Session object, generated in module database. Contains the database path. 
    output: object
        output object --> contains the jobad """
    
    if mode == "overwrite":
        __check_once()
        session.add(output)
    else:
        session.add(output)
    

# Private function to check if needed table already exists, else drop it and create a new empty table
def __check_once():
    global is_created
    if is_created is None:
        try:
            ClassifyUnits.__table__.create(engine)
        except sqlalchemy.exc.OperationalError:
            print("table does already exist")
            ClassifyUnits.__table__.drop(engine)
            ClassifyUnits.__table__.create(engine)
            pass
        is_created = 'checked'
    else:
        pass

    """ def get_traindata(session):
    data = session.query(TrainingData).all()
    return data """

    """ try:
        existing_user = session.query(OutputData).all()
        if existing_user is None:
            session.add(user)  # Add the user
            session.commit()  # Commit the change
            LOGGER.success(f"Created user: {user}")
        else:
            LOGGER.warning(f"Users already exists in database: {existing_user}")
        return session.query(User).filter(User.username == user.username).first()
    except IntegrityError as e:
        LOGGER.error(e.orig)
        raise e.orig
    except SQLAlchemyError as e:
        LOGGER.error(f"Unexpected error when creating user: {e}")
        raise e """
