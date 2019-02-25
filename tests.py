import unittest
from unittest.mock import patch
import unittest.mock as mock
import os

from peewee import *
from datetime import datetime

import work_log
import menus

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([work_log.Entry], safe=True)

DATA = {
    "employee": "Scotty",
    "duration": 3000,
    "task": "Reading",
    "notes": "No notes",
    "date": "21/10/1983"
}

DATA_name = {
    "employee": "Big B",
    "duration": 3000,
    "task": "Reading",
    "notes": "No notes",
    "date": "21/10/1983"
}


class GetTests(unittest.TestCase):

    def test_initialize_database(self):
        """Test the creation of the database"""
        work_log.db.close()
        work_log.initialize()
        self.assertTrue(os.path.isfile('work_log.db'))

    def test_no_results(self):
        self.assertEqual(work_log.no_results(), None)


    def test_clear(self):
        self.assertEqual(work_log.clear(), None)

    def test_get_employee(self):
        to_pass_in = ['a']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_employee()
        self.assertEqual(result, 'a')


    def test_get_date(self):
        to_pass_in = ['01/01/2001']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_date()
        self.assertEqual(result, '01/01/2001')


    # def test_get_date_error(self):
    #     to_pass_in = ['f']
    #     with patch('builtins.input', side_effect=to_pass_in):
    #         with patch('builtins.input', side_effect=print) as mock:
    #             result = work_log.get_date()
    #             mock.assert_called_once_with("Must be in correct DD/MM/YYYY format.")


    def test_get_task(self):
        to_pass_in = ['a']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_task()
        self.assertEqual(result, 'a')


    def test_get_duration(self):
        to_pass_in = ['5']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_duration()
        self.assertEqual(result, '5')



if __name__ == '__main__':
    unittest.main()
