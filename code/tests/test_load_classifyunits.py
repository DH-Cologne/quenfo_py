import unittest

import orm_handling
from database import connection
from orm_handling.models import ClassifyUnits, ExtractionUnits, InformationEntity
from orm_handling.orm import get_classify_units


class TestLoadClassifyUnits(unittest.TestCase):
    def test_table_data(self):
        classify_units = connection.session.query(ClassifyUnits)
        self.assertIsNotNone(classify_units, "Table from database is empty.")

    def test_create_new_table(self):
        if connection.session.query(ExtractionUnits) is None:
            get_classify_units()
            self.assertIsNotNone(connection.session.query(ExtractionUnits), "Table extraction_units in database does "
                                                                            "not exist.")

        if connection.session.query(InformationEntity) is None:
            get_classify_units()
            self.assertIsNotNone(connection.session.query(InformationEntity), "Table extractions in database does "
                                                                              "not exist.")

    def test_type_of_classify_units(self):
        output = orm_handling.orm.get_classify_units()
        self.assertIsInstance(output, list)
        if not any(isinstance(item, ClassifyUnits) for item in output):
            print("List is not type ClassifyUnits.")


if __name__ == '__main__':
    unittest.main()
