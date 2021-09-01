"""Script to build data and to create data"""

# ## Imports
from sqlalchemy.orm import Session
from configuration.config_model import Configurations
from .models import ClassifyUnits, ClassifyUnits_Train, TrainingData, JobAds
from training.train_models import Model
import sqlalchemy
from database import engine, engine2, session2, session
from pathlib import Path
import datetime
import time
import os

# ## Set Variables
is_created = None

# Get Configuration Settings from config.yaml file 
# query_limit: Number of JobAds to process
query_limit = Configurations.get_query_limit()
# mode: append data or overwrite it
mode = Configurations.get_mode()

# ## Functions

# Function to query the data from the db table
def get_jobads() -> list:
    """ Function manages the data query and instantiates the Schema for the class JobAds in models.py

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
        if mode == 'overwrite':
            session.query(ClassifyUnits).delete()
        # load all related classify units for appending
        else:
            session.query(ClassifyUnits).filter(ClassifyUnits.parent_id == JobAds.id).all()

    except sqlalchemy.exc.OperationalError:
        print("table classify_unit does not exist --> create new one")
        ClassifyUnits.__table__.create(engine)

    pass_output(session)
    
    return job_ads


def get_traindata() -> list:
    """ Function manages the data query and instantiates the Schema for the class TrainingData in models.py

    Returns
    -------
    traindata: list
        Data contains the orm-objects from class TrainingData 
    
    Raises
    ------
    sqlalchemy.exc.OperationalError
        If changes in db are not possible, OperationalError is raised to continue with creation of table"""

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

def handle_td_changes(model: Model) -> None:
    """ Manages the traindata changes.
        a. __delete_filler() --> delete all session adding for traindata. 
        b. __reset_td_info(model) --> reset traindata modification date to the one used in modeling.

    Parameters
    ----------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information

    Raises
    ------
    sqlalchemy.exc.OperationalError
        If changes in db are not possible, OperationalError is raised """

    try:
        # delete all session adds for traindata
        __delete_filler()
        # reset modification date from traindata database to the same saved in model
        __reset_td_info(model)
    except sqlalchemy.exc.OperationalError as err:
        print(f'{err}: No need to delete traindata-filler because traindata didnt get processed (model was already there)')

def __delete_filler():
    # remove all unwanted and in memory stored objects and drop the traindata table
    session2.rollback()
    ClassifyUnits_Train.__table__.drop(engine2)

def __reset_td_info(model: Model):
    """ 
    If a new model was trained, the passed object is filled and it contains the actual_timestamp.
        --> The actual_timestamp is set as last modification date for traindata-file
        --> Important because the Traindata file is closed in the previous step and thereby gets new modification date 
        which differs from actual_timestamp.

    Parameters
    ----------
    model: Model
        Class Model consists of tfidf_vectorizer, knn_model (further information about class in orm_handling/models.py) 
        and traindata-information

    Raises
    ------
    IndexError
        If model is not filled or no date could be set, IndexError is raised """
 
    try:
        # Get traindata_path --> to reset last mod. date
        traindata_path = Path(Configurations.get_traindata_path())
        # Define actual_date stored in model
        actual_date = model.traindata_date

        # Split actual date in time-components
        year, month, day = (actual_date.split(' ')[0]).split('-')
        hour, minute, second = (actual_date.split(' ')[1]).split(':')

        # Set it as datetime object
        date = datetime.datetime(year=int(year), month=int(month), day=int(day), \
            hour=int(hour), minute=int(minute), second=int(second), microsecond=0)
        modTime = time.mktime(date.timetuple())
        # Set acutal time as last modification date for traindata-file
        os.utime(traindata_path, (modTime, modTime))
    except IndexError:
        pass

def pass_output(session: Session):
    """ The session.commit() statement commits all adds to the current session.

    Parameters
    ----------
    session: Session
        Session object, generated in module database. Contains the database path. """

    session.commit()

def close_session(session: Session):
    """ The session.close() statement closes the current session.

    Parameters
    ----------
    session: Session
        Session object, generated in module database. Contains the database path. """

    session.close()

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