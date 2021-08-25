import unittest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from database import connection


class TestDBConnection(unittest.TestCase):
    def test_session(self):
        self.assertIsInstance(connection.session, Session, "Session to database is not ready.")

    def test_engine(self):
        self.assertIsInstance(connection.engine, Engine, "Engine from session is not ready.")


if __name__ == '__main__':
    unittest.main()
