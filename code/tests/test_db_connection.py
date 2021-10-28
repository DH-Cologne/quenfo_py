from logging import raiseExceptions
import unittest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import database
import configuration

method_args = {'input_path': 'C:\\Users\\Anne\\Desktop\\Quenfo\\quenfo_py_data\\sqlite\\orm\\text_kernel_orm_2018_03.db', 'db_mode': 'append'}

class TestDBConnection(unittest.TestCase):

    configuration.set_config(method_args)
    
    def test_input_path(self):
        path = method_args['input_path']
        self.assertNotIsInstance(path, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                               "db-path is"
                                                                                               " not string.")
        self.assertIsInstance(path, str)
        self.assertRegex(path, ".*db$", "Path does not end with string 'db' and is not the path to a database.")
    
    
    def test_db_mode(self):
        mode = method_args['db_mode']
        self.assertNotIsInstance(mode, (int, float, complex, list, tuple, range, bool, bytes), "Type of "
                                                                                               "mode is"
                                                                                               " not string.")
        self.assertIsInstance(mode, str)
        self.assertTrue(any(i in (mode) for i in ('overwrite', 'append')))
    
    database.set_input_conn()
    database.set_train_conn()
    
    def test_session(self):
        self.assertIsInstance(database.session, Session, "Session to database is not ready.")
    def test_session2(self):
        self.assertIsInstance(database.session2, Session, "Session to database is not ready.")
    def test_engine(self):
        self.assertIsInstance(database.engine, Engine, "Engine from session is not ready.")
    def test_engine2(self):
        self.assertIsInstance(database.engine2, Engine, "Engine from session is not ready.")


if __name__ == '__main__':
    unittest.main()
