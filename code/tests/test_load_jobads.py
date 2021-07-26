import unittest

import orm_handling.orm
from database import connection
from orm_handling.models import JobAds, ClassifyUnits


class TestGetJobAds(unittest.TestCase):
    def test_table_data(self):
        job_ads = connection.session.query(JobAds)
        self.assertIsNotNone(job_ads, "Table from database is empty.")

    def test_create_new_table(self):
        if connection.session.query(ClassifyUnits) is None:
            orm_handling.orm.get_jobads(connection.session)
            self.assertIsNotNone(connection.session.query(ClassifyUnits), "Table classify_units in database does not "
                                                                          "exist.")

    def test_type_of_jobads(self):
        # TODO: check if object type of list is JobAds
        self.assertIsInstance(orm_handling.orm.get_jobads(connection.session), list)


if __name__ == '__main__':
    unittest.main()
