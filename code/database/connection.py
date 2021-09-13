""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configuration

def set_testdata():
    # ## Input-Paths (Testdata and Traindata)
    input_path = configuration.config_obj.get_input_path()
    # Create engine with path
    engine = create_engine('sqlite:///' + input_path, echo=False)
    engine.execution_options(stream_results=True)
    # Bind engine to recieve a session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine


def set_traindata():
    traindata_path = configuration.config_obj.get_traindata_path()
    engine2 = create_engine('sqlite:///' + traindata_path, echo=False)
    engine2.execution_options(stream_results=True)
    Session2 = sessionmaker(bind=engine2)
    
    # Instantiate a session object
    session2 = Session2()
    return session2, engine2