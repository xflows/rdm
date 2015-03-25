import unittest
import sys
sys.path.append('..')


from rdm.db import DBConnection, DBContext
from conf import TEST_DB


class TestConverters(unittest.TestCase):

    def setUp(self):
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database']
        )
        self.context = DBContext(self.connection)


    def test_rsd_converter(self):
        self.assertTrue(True)
