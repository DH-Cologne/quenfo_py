import unittest
import orm_handling.orm
import database
from orm_handling.models import JobAds, ClassifyUnits
import configuration

# First preparation-steps to execute following Tests
method_args = {'input_path': 'C:\\Users\\Anne\\Desktop\\Quenfo\\quenfo_py_data\\sqlite\\orm\\text_kernel_orm_2018_03.db', 'db_mode': 'append'}
configuration.set_config(method_args)
database.set_input_conn()
database.set_train_conn()
start_pos = 0
 
### TODO: Die Funktionen aus orm.py austesten. Die erste hier test_table_data kann für get_jobads genutzt wrden.
class TestGetJobAds(unittest.TestCase):
    def test_table_data(self):
        job_ads = database.session.query(JobAds)
        self.assertIsNotNone(job_ads, "Table from database is empty.")

    def test_create_new_table(self):
        if database.session.query(ClassifyUnits) is None:
            orm_handling.orm.get_jobads(start_pos)
            self.assertIsNotNone(database.session.query(ClassifyUnits), "Table classify_units in database does not "
                                                                          "exist.")

    def test_type_of_jobads(self):
        output = orm_handling.orm.get_jobads(start_pos)
        self.assertIsInstance(output, list)
        if not any(isinstance(item, JobAds) for item in output):
            print("List is not type JobAds.")


if __name__ == '__main__':
    unittest.main()