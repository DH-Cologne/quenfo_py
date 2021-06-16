"""Script to build data and to create data"""
from typing import Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql.expression import false, true
from .models import OutputData, TrainingData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from database import engine

is_created = None

def get_traindata(session):
    data = session.query(TrainingData).all()
    return data


def create_output(session, output):
    __check_once()
    session.add(output)
    
    
def __check_once(): 
    global is_created
    if is_created is None:
        try:
            OutputData.__table__.create(engine)
        except sqlalchemy.exc.OperationalError:
            print("table does already exist")
            pass
        is_created = 'checked'
    else:
        pass
        







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