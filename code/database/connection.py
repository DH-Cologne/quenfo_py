""" Script to create a connection to sqlite dbs depending on database-path. """

# ## Imports
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from typing import Union

# ## Function
def create_connection(database_path: str) -> Union[Session, Engine]:
    """ Function creates engine via database_path and binds engine to receive a session.
    
    Parameters
    ----------
    database_path: str
        String contains the Path of the database.
    
    Returns
    -------
    session: Session
        session object
    engine: Engine
        engine object """

    # Create engine with path
    engine = create_engine('sqlite:///' + database_path, echo=False)
    engine.execution_options(stream_results=True)
    # Bind engine to receive a session
    Session = sessionmaker(bind=engine)
    # Instantiate a session object
    session = Session()
    return session, engine