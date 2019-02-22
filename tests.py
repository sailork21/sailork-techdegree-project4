import unittest
from unittest.mock import patch
from unittest.mock import Mock

import work_log

entries = ['1', '2']

class GetTests(unittest.TestCase):

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


    def test_get_date_error(self):
        to_pass_in = ['f']
        with patch('builtins.input', side_effect=to_pass_in):
            with patch('builtins.input', side_effect=print) as mock:
                result = work_log.get_date()
                mock.assert_called_once_with("Must be in correct DD/MM/YYYY format.")


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
