""" Script is the intermediary between the database and the data-handling.
    --> The data loading and handling takes place here and the modified data to be saved in the database is handled here too."""

# ## Imports
from information_extraction.models import ExtractedEntity
from .models import ClassifyUnits, ClassifyUnits_Train, TrainingData, JobAds, ExtractionUnits, InformationEntity
from training.train_models import Model
import sqlalchemy
import database
from pathlib import Path
import datetime
import time
import os
import configuration
from sqlalchemy.orm import Session
from sqlalchemy import func
import logger
from sqlalchemy import inspect

# ## Set Variables
is_created = None
drop_once_c = None
drop_once_eu = None
drop_once_e = None


# ## Functions

# Function to query the data from the db table
def get_jobads(current_pos: int) -> list:
    """ Function manages the data query and instantiates the Schema for the class JobAds in models.py

    Parameters
    ----------
    current_pos: int
        The integer contains the current position in database (rownr)

    Returns
    -------
    jobads: list
        Data contains the orm-objects from class JobAds 
    
    Raises
    ------
    sqlalchemy.exc.OperationalError
        If changes in db are not possible, OperationalError is raised to continue with creation of table """

    # Set global
    global drop_once_c

    # Get Configuration Settings from config.yaml file 
    fetch_size = configuration.config_obj.get_c_fetch_size()  # Number of JobAds to fetch in one query
    db_mode = configuration.config_obj.get_mode()  # db_mode: append data or overwrite it

    # load the jobads
    # job_ads = database.session.query(JobAds).slice(current_pos, (current_pos+fetch_size)).all()            # 0:02:26.691769 bei 2500 JobAds and 0:16:07.362719 bei 9593
    job_ads = database.session.query(JobAds).order_by('id').offset(current_pos).limit(fetch_size).all()      # 0:02:25.670638 bei 2500 JobAds and 0:14:19.315887 bei 9593
    # job_ads = database.session.query(JobAds).where(current_pos<(current_pos+fetch_size)).all()             # 0:02:21.205672 bei 2500 JobAds and 0:13:37.800832 bei 9593

    try:
        # delete the handles from jobads to classifyunits or create new table
        if db_mode == 'overwrite':
            if drop_once_c is None:
                try:
                    ClassifyUnits.__table__.create(database.engine)
                except sqlalchemy.exc.OperationalError as err:
                    database.session.query(ClassifyUnits).delete()
                drop_once_c = 'filled'
            else:
                pass
        # load all related classify units for appending
        else:
            if inspect(database.engine).has_table(
                    ClassifyUnits.__tablename__):  # if table does exist, get related units
                database.session.query(ClassifyUnits).filter(ClassifyUnits.parent_id == JobAds.id).all()
            else:  # else: create classifyunits table
                ClassifyUnits.__table__.create(database.engine)  # for case that table does exist, but is empty
    except sqlalchemy.exc.OperationalError:
        logger.log_clf.info(f'Table classify_unit does not exist --> create new one')
        ClassifyUnits.__table__.create(database.engine)

    pass_output(database.session)

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
    traindata = database.session2.query(TrainingData).all()

    try:
        ClassifyUnits_Train.__table__.create(database.engine2)
    except sqlalchemy.exc.OperationalError:
        logger.log_clf.info(f'ClassifyUnits_Train table already there, drop it.')
        ClassifyUnits_Train.__table__.drop(database.engine2)
        ClassifyUnits_Train.__table__.create(database.engine2)
        pass

    # return Trainindata objects as list
    return traindata


def get_classify_units(current_pos: int) -> list:
    """ Function manages the data query and instantiates the Schema for the class ClassifyUnits in models.py

    Parameters
    ----------
    current_pos: int
        The integer contains the current position in database (rownr)

    Returns
    -------
    classify_units: list
        Data contains the orm-objects from class ClassifyUnits

    Raises
    ------
    sqlalchemy.exc.OperationalError
        If changes in db are not possible, OperationalError is raised to continue with creation of table """

    # Set global
    global drop_once_eu

    # Get Configuration Settings from config.yaml file
    fetch_size = configuration.config_obj.get_ie_fetch_size()  # Number of ClassifyUnits to fetch in one query
    db_mode = configuration.config_obj.get_mode()  # db_mode: append data or overwrite it
    search_type = configuration.config_obj.get_search_type()

    # load the cus
    classify_units = database.session.query(ClassifyUnits).order_by('id').filter(
        ClassifyUnits.classID == search_type).offset(current_pos).limit(fetch_size).all()

    try:
        # delete the handles from classifyunits to extractionunits or create new table
        if db_mode == 'overwrite':
            if drop_once_eu is None:
                try:
                    ExtractionUnits.__table__.create(database.engine)
                except sqlalchemy.exc.OperationalError as err:
                    database.session.query(ExtractionUnits).delete()
                drop_once_eu = 'filled'
            else:
                pass
        # load all related extractionunits for appending
        else:
            if inspect(database.engine).has_table(
                    ExtractionUnits.__tablename__):  # if table does exist, get related units
                database.session.query(ExtractionUnits).filter(ExtractionUnits.parent_id == ClassifyUnits.id).all()
            else:  # else: create extractionunit table
                ExtractionUnits.__table__.create(database.engine)
    except sqlalchemy.exc.OperationalError:
        logger.log_ie.info(f'table extraction_units does not exist --> create new one')
        ExtractionUnits.__table__.create(database.engine)

    pass_output(database.session)

    return classify_units


def get_extraction_units() -> list:
    """ Function manages the data query and instantiates the Schema for the class ExtractionUnits in models.py

        Returns
        -------
        extraction_units: list
            Data contains the orm-objects from class ExtractionUnits

        Raises
        ------
        sqlalchemy.exc.OperationalError
            If changes in db are not possible, OperationalError is raised to continue with creation of table """

    # Set global
    global drop_once_e

    # Get Configuration Settings from config.yaml file
    db_mode = configuration.config_obj.get_mode()  # db_mode: append data or overwrite it

    # load the eus
    extraction_units = database.session.query(ExtractionUnits).order_by('id').all()

    try:
        # delete the handles from extractionunits to extractions or create new table
        if db_mode == 'overwrite':
            if drop_once_e is None:
                try:
                    ExtractedEntity.__table__.create(database.engine)
                except sqlalchemy.exc.OperationalError as err:
                    database.session.query(ExtractedEntity).delete()
                drop_once_e = 'filled'
            else:
                pass
        # load all related InformationEntity for appending
        else:
            if inspect(database.engine).has_table(
                    ExtractedEntity.__tablename__):  # if table does exist, get related units
                database.session.query(ExtractedEntity).filter(
                    ExtractedEntity.parent_id == ExtractionUnits.id).all()
            else:  # else: create extractionunit table
                ExtractedEntity.__table__.create(database.engine)
    except sqlalchemy.exc.OperationalError:
        logger.log_ie.info(f'table extracted_entities does not exist --> create new one')
        ExtractedEntity.__table__.create(database.engine)

    pass_output(database.session)

    return extraction_units


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
        logger.log_clf.info(f'Reset added traindata-obj in current session and reset modification date from traindata. \
            Because: Traindata was used to train new model, but while loading and using traindata the modification date changed. \
                But the last modification date was stored in model for later checkup. If date is not reset, traindata and model never match.')
    except sqlalchemy.exc.OperationalError as err:
        logger.log_clf.info(f'{err}: No need to delete traindata-filler because traindata \
            didnt get processed because model was already there. Error message can be ignored.')


def __delete_filler() -> None:
    """ Remove all unwanted and in memory stored Traindata-objects and drop the traindata table. Nothing is modified in those tables."""

    # rollback
    database.session2.rollback()
    # drop the table
    ClassifyUnits_Train.__table__.drop(database.engine2)


def __reset_td_info(model: Model) -> None:
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
        traindata_path = Path(configuration.config_obj.get_traindata_path())
        # Define actual_date stored in model
        actual_date = model.traindata_date

        # Split actual date in time-components
        year, month, day = (actual_date.split(' ')[0]).split('-')
        hour, minute, second = (actual_date.split(' ')[1]).split(':')

        # Set it as datetime object
        date = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                                 second=int(second), microsecond=0)
        modTime = time.mktime(date.timetuple())
        # Set actual time as last modification date for traindata-file
        os.utime(traindata_path, (modTime, modTime))
    except (IndexError, ValueError):
        pass


def get_length(table_type: str) -> int:
    """ The function gets the number of JobAds in the database table.

    Parameters
    ----------
    table_type: str
        Keyword with selected database-table.

    Returns
    -------
    row_nrs: int
        Integer with the count of all JobAds or ClassfiyUnits in table. """
    row_nrs = int()
    if table_type.__eq__('ad'):
        row_nrs = database.session.query(func.count(JobAds.id)).scalar()
    elif table_type.__eq__('cu'):
        row_nrs = database.session.query(func.count(ClassifyUnits.id)).scalar()
    return row_nrs


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
def create_output(session: Session, output: object, table_type: str):
    """ Function checks if table to store output in already exists. Else the table is dropped and created again.
    The session.add(object) statement adds the passed object to the current session.

    Parameters
    ----------
    table_type: str
        Name of the database table to create.
    session: Session
        Session object, generated in module database. Contains the database path. 
    output: object
        output object --> contains the jobad """

    # db_mode: append data or overwrite it
    db_mode = configuration.config_obj.get_mode()
    
    if db_mode == "overwrite":
        __check_once(table_type)
        session.add(output)
    else:
        session.add(output)


# Private function to check if needed table already exists, else drop it and create a new empty table
def __check_once(table_type: str):

    # Set global
    global is_created

    # Set switch-variable for db-table and logger
    switch_table = {
        'cu': ClassifyUnits,
        'eu': ExtractionUnits,
        'e': InformationEntity,
        # 'me': MatchedEntity
    }
    switch_logger = {
        'cu': logger.log_clf,
        'eu': logger.log_ie,
        'e': logger.log_ie,
        # 'me': logger.log_m,
    }

    # Set variable
    table_name = switch_table.get(table_type)
    log_name = switch_logger.get(table_type)

    if is_created is None:
        try:
            table_name.__table__.create(database.engine)
        except sqlalchemy.exc.OperationalError:
            log_name.info(f'Table {table_name} does already exist. Will be dropped, because of overwrite mode.')
            table_name.__table__.drop(database.engine)
            table_name.__table__.create(database.engine)
            pass
        is_created = 'checked'
    else:
        pass
