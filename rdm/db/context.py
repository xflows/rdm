from collections import defaultdict
import pprint
import copy

import mysql.connector as mysql
import psycopg2 as postgresql
import converters

from datasource import MySQLDataSource, PgSQLDataSource


class DBVendor:
    MySQL = 'mysql'
    PostgreSQL = 'postgresql'


class DBConnection:
    '''
    Database credentials.
    '''

    class Manager:
        '''
        Context Manager.
        '''
        def __init__(self, user, password, host, database, dal_connect_fun):
            self.con = dal_connect_fun(
                user=user,
                password=password,
                host=host, 
                database=database
            )

        def __enter__(self):
            return self.con

        def __exit__(self, exc_type, exc_value, traceback):
            self.con.close()


    def __init__(self, user, password, host, database, vendor=DBVendor.MySQL):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.vendor = vendor
        self.check_connection()

        if self.vendor == DBVendor.MySQL:
            self.src = MySQLDataSource(self)
        elif self.vendor == DBVendor.PostgreSQL:
            self.src = PgSQLDataSource(self)
        else:
            raise Exception("Unknown DB vendor: {}".format(vendor))


    def check_connection(self):
        try:
            with self.connect() as _:
                pass
        except Exception,e:
            raise Exception('Problem connecting to the database. Please re-check your credentials.')


    def connection(self):
        return self.connect().con


    def connect(self):
        if self.vendor == DBVendor.MySQL:
            dal_connect_fun = mysql.connect
        elif self.vendor == DBVendor.PostgreSQL:
            dal_connect_fun = postgresql.connect

        return DBConnection.Manager(self.user, self.password, self.host, self.database, dal_connect_fun)


class DBContext:
    def __init__(self, connection, find_connections=False, in_memory=True):
        '''
        @connection: a DBConnection instance.

        Initializes the fields:
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
        self.src = connection.src
        self.tables = self.src.tables()
        self.cols = {}
        for table in self.tables:
            self.cols[table] = self.src.table_columns(table)

        self.all_cols = dict(self.cols)
        self.col_vals = {}

        conn_data = self.src.connected(
            self.tables,
            self.cols,
            find_connections=find_connections
        )
        self.connected, self.pkeys, self.fkeys, self.reverse_fkeys = conn_data

        self.target_table = self.tables[0]
        self.target_att = None

        self.orng_tables = None
        self.in_memory = in_memory


    def read_into_orange(self):
        conv = converters.OrangeConverter(self)
        tables = {
            self.target_table: conv.target_Orange_table()
        }
        other_tbl_names = [table for table in self.tables if table != self.target_table]
        other_tables = dict(zip(other_tbl_names, conv.other_Orange_tables()))
        tables.update(other_tables)
        return tables


    def fetch(self, table, cols):
        '''
        Fetches rows from the db.
        '''
        return self.src.fetch(table, cols)


    def rows(self, table, cols):
        '''
        Fetches rows from the local cache or from the db if there's no cache.
        '''
        if self.orng_tables:
            data = []
            for ex in self.orng_tables[table]:
                data.append([ex[str(col)] for col in cols])
            return data
        else:
            return self.fetch(table, cols)


    def select_where(self, table, cols, pk_att, pk):
        '''
        SELECT with WHERE clause.
        '''
        if self.orng_tables:
            data = []
            for ex in self.orng_tables[table]:
                if str(ex[str(pk_att)]) == str(pk):
                    data.append([ex[str(col)] for col in cols])
            return data
        else:
            return self.src.select_where(table, cols, pk_att, pk)


    def fetch_types(self, table, cols):
        '''
        Returns a dictionary of field types for the given table and columns.
        '''
        return self.src.fetch_types(table, cols)


    def compute_col_vals(self):
        for table, cols in self.cols.items():
            self.col_vals[table] = {}
            for col in cols:
                self.col_vals[table][col] = self.src.column_values(table, col)


    def copy(self):
        return copy.deepcopy(self)


    def __repr__(self):
        return pprint.pformat({
            'target_table' : self.target_table, 
            'target attribute' : self.target_att, 
            'tables' : self.tables, 
            'cols' : self.cols, 
            'connected' : self.connected, 
            'pkeys' : self.pkeys, 
            'fkeys' : self.fkeys,
            'orng_tables': [(name, len(table)) for name, table in self.orng_tables.items()] if self.orng_tables else 'not in memory'
        })
