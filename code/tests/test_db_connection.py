import unittest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import repackage
repackage.up()
from database import session, session2, engine, engine2


class TestDBConnection(unittest.TestCase):
    def test_session(self):
        # TODO: Hier noch als beispiel den pfad zu einer db mitgeben und database.set_input_path aufrufen, dann überprüfen ob session ready ist.
        self.assertIsInstance(session, Session, "Session to database is not ready.")
    def test_session2(self):
        self.assertIsInstance(session2, Session, "Session to database is not ready.")
    def test_engine(self):
        self.assertIsInstance(engine, Engine, "Engine from session is not ready.")
    def test_engine2(self):
        self.assertIsInstance(engine2, Engine, "Engine from session is not ready.")


if __name__ == '__main__':
    unittest.main()
