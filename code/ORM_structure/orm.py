"""Script to build data and to create data"""

# ## Imports
from sqlalchemy.orm import Session
from .models import ClassifyUnits, OutputData, TrainingData, JobAds
import sqlalchemy
from database import engine

# ## Variables
is_created = None

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
        Data contains the orm-objects from class JobAds """
        
    """ ClassifyUnits.__table__.drop(engine)
    ClassifyUnits.__table__.create(engine) """
    
    job_ads = session.query(JobAds).limit(500).all()
    # delete the handles from jobads to classifunit
    session.query(ClassifyUnits).delete()
    session.commit()
    
    return job_ads
    
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
        Session object, generated in module database. Contains the database path. """

    __check_once()
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