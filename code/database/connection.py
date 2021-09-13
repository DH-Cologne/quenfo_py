""" Script to create a connection to sqlite dbs depending on input path. """

# ## Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_connection(database_path):
    # Create engine with path
    engine = create_engine('sqlite:///' + database_path, echo=False)
    engine.execution_options(stream_results=True)
    # Bind engine to recieve a session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine
