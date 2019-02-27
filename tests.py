import unittest
from unittest.mock import patch
import unittest.mock as mock
import os

from peewee import *
from datetime import datetime

import work_log
import menus

TEST_DB = SqliteDatabase(':memory:')

entries = {
    'date': '21/10/1983',
    'employee': 'Scott',
    'task': 'None',
    'duration': 5,
    'notes': 'none'
    }

class GetTests(unittest.TestCase):

    def setUp(self):
        TEST_DB.bind([work_log.Entry])
        TEST_DB.create_tables([work_log.Entry], safe=True)
        # TEST_DB.connect()


    def test_initialize_database(self):
        work_log.db.close()
        work_log.initialize()
        self.assertTrue(os.path.isfile('work_log.db'))


    def test_no_results(self):
        self.assertEqual(work_log.no_results(), None)


    def test_get_employee(self):
        to_pass_in = ['a']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_employee()
        self.assertEqual(result, 'a')


    def test_get_date(self):
        to_pass_in = ['01/01/2001']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_date()
        self.assertNotEqual(result, '01/01/2001')


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


    def test_entry_data(self):
        to_pass_in = ['21/10/1983', 'b', 'c', '5', 'e']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.entry_data()
        self.assertEqual(result, None)


    def test_search_employee_name(self):
        to_pass_in = ['Scott']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_employee_name()
        assert result == None


    def test_search_duration(self):
        to_pass_in = ['50']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_duration()
        assert result == None


    def test_search_exact(self):
        to_pass_in = ['50']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_exact()
        assert result == None


    def test_get_employee_error(self):
        to_pass_in = ['a']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_employee(error='true')
        assert result != None


    def test_get_date_none(self):
        to_pass_in = ['21/10/1983']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_date(error='true')
        assert result != None


    def test_get_task_none(self):
        to_pass_in = ['test']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_task(error='true')
        assert result != None


    def test_get_duration(self):
        to_pass_in = ['5']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.get_duration(error='true')
        assert result != None


    def test_search_duration(self):
        to_pass_in = ['10']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_duration()
        assert result == None

    def test_search_duration2(self):
        to_pass_in = ['10']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_duration2()
        assert result == None


    def test_search_exact(self):
        to_pass_in = ['10']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_exact()
        assert result == None


    def test_date_range(self):
        to_pass_in = ['01/01/2001', '01/01/2001']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_date_range()
        assert result == None


    def test_search_employee_name(self):
        to_pass_in = ['a']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = work_log.search_employee_name()
        assert result == None


    def test_main_menu(self):
        to_pass_in = ['c']
        with patch('builtins.input', side_effect=to_pass_in) as mock:
            result = menus.main_menu()
        assert result == None


if __name__ == '__main__':
    unittest.main()
