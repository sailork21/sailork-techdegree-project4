import unittest

import work_log


class WorkLogTests(unittest.TestCase):

    def test_main(self):
        self.assertNotEqual(work_log.main_menu(), 'n')



if __name__ == '__main__':
    unittest.main()
