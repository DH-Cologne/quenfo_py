import unittest

import database
from orm_handling.models import JobAds, ClassifyUnits


class TestLoadTablesFromDB(unittest.TestCase):
    """def test_table_data(self):
        job_ads = database.session.query(JobAds)
        self.assertIsNotNone(job_ads, 'Table job_ads does not exist.')

        classify_units = database.session(ClassifyUnits)
        self.assertIsNotNone(classify_units, 'Table classify_units does not exist.')

    def test_create_new_table(self):
        if database.session.query(ClassifyUnits) is None:
            orm_handling.orm.get_jobads()
            self.assertIsNotNone(database.session.query(ClassifyUnits), "Table classify_units in database does not "
                                                                        "exist.")

    def test_type_of_jobads(self):
        output = orm_handling.orm.get_jobads()
        self.assertIsInstance(output, list)
        if not any(isinstance(item, JobAds) for item in output):
            print("List is not type JobAds.")


    def test_create_new_table(self):
        if database.session.query(ExtractionUnits) is None:
            get_classify_units()
            self.assertIsNotNone(database.session.query(ExtractionUnits), "Table extraction_units in database does "
                                                                            "not exist.")

        if database.session.query(InformationEntity) is None:
            get_classify_units()
            self.assertIsNotNone(database.session.query(InformationEntity), "Table extractions in database does "
                                                                              "not exist.")

    def test_type_of_classify_units(self):
        output = orm_handling.orm.get_classify_units()
        self.assertIsInstance(output, list)
        if not any(isinstance(item, ClassifyUnits) for item in output):
            print("List is not type ClassifyUnits.")"""


if __name__ == '__main__':
    unittest.main()
