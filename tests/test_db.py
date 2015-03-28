import unittest
import sys
sys.path.append('..')


from rdm.db import DBConnection, DBContext
from conf import TEST_DB


class TestConnection(unittest.TestCase):

    def test_mysql(self):
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database']
        )
        try:
            self.connection.check_connection()
            connection_success = True
        except:
            connection_success = False
        self.assertTrue(connection_success)


class TestContext(unittest.TestCase):

    def setUp(self):
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database']
        )

    def test_db_read(self):
        '''
            tables:           list of selected tables
            cols:             dict of columns for each table
            all_cols:         dict of columns for each table (even unselected)
            col_vals:         available values for each table/column 
            connected:        dict of table pairs and the connected columns
            fkeys:            foreign keys in a given table
            reverse_fkeys:    fkey to table map
            pkeys:            private key for a given table
            target_table:     selected table for learning
            target_att:       selected column for learning
        '''
        self.context = DBContext(self.connection)
        self.assertListEqual(self.context.tables, ['cars', 'trains'])
        self.assertTrue(('cars', 'trains') in self.context.connected)
