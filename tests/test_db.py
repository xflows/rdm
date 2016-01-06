import unittest
import sys
sys.path.append('..')


from rdm.db import DBVendor, DBConnection, DBContext, MySQLDataSource
from conf import TEST_DB, TEST_DB_POSTGRES


class TestConnection(unittest.TestCase):

    def test_mysql(self):
        self.connection = DBConnection(
            TEST_DB['user'],
            TEST_DB['pass'],
            TEST_DB['host'],
            TEST_DB['database'],
            vendor=TEST_DB['vendor']
        )
        try:
            self.connection.check_connection()
            connection_success = True
        except:
            connection_success = False
        self.assertTrue(connection_success)


    def test_pgsql(self):
        self.connection = DBConnection(
            TEST_DB_POSTGRES['user'],
            TEST_DB_POSTGRES['pass'],
            TEST_DB_POSTGRES['host'],
            TEST_DB_POSTGRES['database'],
            vendor=TEST_DB_POSTGRES['vendor']
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
            TEST_DB['database'],
            vendor=TEST_DB['vendor']
        )

        self.connection_pg = DBConnection(
            TEST_DB_POSTGRES['user'],
            TEST_DB_POSTGRES['pass'],
            TEST_DB_POSTGRES['host'],
            TEST_DB_POSTGRES['database'],
            vendor=TEST_DB_POSTGRES['vendor']
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
        self.assertItemsEqual(self.context.tables, ['cars', 'trains'])
        self.assertTrue(('cars', 'trains') in self.context.connected)

        self.context = DBContext(self.connection_pg)
        self.assertItemsEqual(self.context.tables, ['building', 'urbanblock'])
        self.assertTrue(('building', 'urbanblock') in self.context.connected)
