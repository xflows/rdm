from collections import defaultdict
from exceptions import NotImplementedError
import mysql.connector as mysql


class DataSource:
    '''
    A data abstraction layer for accessing datasets.

    This layer is typically hidden from end-users, as they only access
    the database through DBConnection and DBContext objects.
    '''

    def connect(self):
        '''
            :return: a connection object.
            :rtype: DBConnection
        '''
        raise NotImplementedError()

    def tables(self):
        '''
            :return: a list of table names.
            :rtype: list
        '''
        raise NotImplementedError()

    def table_columns(self, table_name):
        '''
            :param table_name: table name for which to retrieve column names
            :return: a list of columns for the given table.
            :rtype: list
        '''
        raise NotImplementedError()

    def foreign_keys(self):
        '''
            :return: a list of foreign key relations in the form (table_name, column_name, referenced_table_name, referenced_column_name).
            :rtype: list
        '''
        raise NotImplementedError()

    def table_column_names(self):
        '''
            :return: a list of table / column names in the form (table, col_name).
            :rtype: list
        '''
        raise NotImplementedError()

    def connected(self, tables, cols, find_connections=False):
        '''
        Returns a list of tuples of connected table pairs.

            :param tables: a list of table names
            :param cols: a list of column names
            :param find_connections: set this to True to detect relationships from column names.

            :return: a tuple (connected, pkeys, fkeys, reverse_fkeys)
        '''
        connected = defaultdict(list)
        fkeys = defaultdict(set)
        reverse_fkeys = {}
        pkeys = {}
        with self.connect() as con:
            fk_result = self.foreign_keys()
            if find_connections:
                for table in tables:
                    for col in cols[table]:
                        if col.endswith('_id'):
                            ref_table = (col[:-4] + 'ies') if col[-4] == 'y' and col[-5] != 'e' else (col[:-3] + 's')
                            if ref_table in tables:
                                connected[(table, ref_table)].append((col, 'id'))
                                connected[(ref_table, table)].append(('id', col))
                                fkeys[table].add(col)
                                reverse_fkeys[(table, col)] = ref_table
                        if col == 'id':
                            pkeys[table] = col
            for (table, col, ref_table, ref_col) in fk_result:
                connected[(table, ref_table)].append((col, ref_col))
                connected[(ref_table, table)].append((ref_col, col))
                fkeys[table].add(col)
                reverse_fkeys[(table, col)] = ref_table

            tbl_col_names = self.table_column_names()
            for (table, pk) in tbl_col_names:
                pkeys[table] = pk

        return connected, pkeys, fkeys, reverse_fkeys

    def table_primary_key(self, table_name):
        '''
        Returns the primary key attribute name for the given table.

            :param table_name: table name string
        '''
        raise NotImplementedError()

    def fetch(self, table, cols):
        '''
        Fetches rows for the given table and columns.

            :param table: target table
            :param cols: list of columns to select
            :return: rows from the given table and columns
            :rtype: list
        '''
        raise NotImplementedError()

    def select_where(self, table, cols, pk_att, pk):
        '''
        Select with where clause.

            :param table: target table
            :param cols: list of columns to select
            :param pk_att: attribute for the where clause
            :param pk: the id that the pk_att should match
            :return: rows from the given table and cols, with the condition pk_att==pk
            :rtype: list
        '''
        raise NotImplementedError()

    def fetch_types(self, table, cols):
        '''
        Returns a dictionary of field types for the given table and columns.

            :param table: target table
            :param cols: list of columns to select
            :return: a dictionary of types for each attribute
            :rtype: dict
        '''
        raise NotImplementedError()

    def column_values(self, table, col):
        '''
        Returns a list of distinct values for the given table and column.

            :param table: target table
            :param cols: list of columns to select
        '''
        raise NotImplementedError()

    def get_driver_name(self):
        raise NotImplementedError()

    def get_jdbc_prefix(self):
        raise NotImplementedError()


class MySQLDataSource(DataSource):
    '''
    A DataSource implementation for accessing datasets from a MySQL DBMS.
    '''

    def __init__(self, connection):
        '''
            :param connection: a DBConnection instance.
        '''
        self.connection = connection

    def connect(self):
        return self.connection.connect()

    def foreign_keys(self):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute(
               "SELECT table_name, column_name, referenced_table_name, referenced_column_name \
                FROM information_schema.KEY_COLUMN_USAGE \
                WHERE referenced_table_name IS NOT NULL AND table_schema='%s'" % self.connection.database)
            fk_result = [row for row in cursor]
        return fk_result

    def table_column_names(self):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT table_name, column_name \
                 FROM information_schema.KEY_COLUMN_USAGE \
                 WHERE constraint_name='PRIMARY' AND table_schema='%s'" % self.connection.database)
            tbl_col_names = [row for row in cursor]
        return tbl_col_names

    def tables(self):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute('SHOW tables')
            tables = [table for (table,) in cursor]
        return tables

    def table_columns(self, table_name):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '%s' AND table_schema='%s'" % (table_name, self.connection.database))
            columns = [col for (col,) in cursor]
        return columns

    def fmt_cols(self, cols):
        return ','.join(["`%s`" % col for col in cols])

    def fetch_types(self, table, cols):
        with self.connect() as con:
            cursor = con.cursor() 
            cursor.execute("SELECT %s FROM `%s` LIMIT 1" % (self.fmt_cols(cols), table))
            cursor.fetchall()
            types = {}
            for desc in cursor.description:
                types[desc[0]] = mysql.FieldType.get_info(desc[1])
        return types

    def fetch(self, table, cols):
        with self.connect() as con:
            cursor = con.cursor() 
            cursor.execute("SELECT %s FROM %s" % (self.fmt_cols(cols), table))
            result = [cols for cols in cursor]
        return result

    def select_where(self, table, cols, pk_att, pk):
        with self.connect() as con:
            cursor = con.cursor() 
            attributes = self.fmt_cols(cols)
            cursor.execute("SELECT %s FROM %s WHERE `%s`='%s'" % (attributes, table, pk_att, pk))
            result = [cols for cols in cursor]
        return result

    def column_values(self, table, col):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute("SELECT DISTINCT BINARY `%s`, `%s` FROM `%s`" % (col, col, table))
            values = [val for (_,val) in cursor]
        return values

    def get_driver_name(self):
        return 'com.mysql.jdbc.Driver'

    def get_jdbc_prefix(self):
        return 'jdbc:mysql://'


class PgSQLDataSource(DataSource):
    '''
    A DataSource implementation for accessing datasets from a PosgreSQL DBMS.
    '''
    def __init__(self, connection):
        '''
            :param connection: a DBConnection instance.
        '''
        self.connection = connection

    def connect(self):
        return self.connection.connect()

    def foreign_keys(self):
        with self.connect() as con:
            cursor = con.cursor()
            database = self.connection.database
            cursor.execute("SELECT \
                    tc.table_name, kcu.column_name, \
                    ccu.table_name AS referenced_table_name,\
                    ccu.column_name AS referenced_column_name \
                    FROM \
                    information_schema.table_constraints AS tc \
                    JOIN information_schema.key_column_usage AS kcu \
                      ON tc.constraint_name = kcu.constraint_name \
                    JOIN information_schema.constraint_column_usage AS ccu \
                      ON ccu.constraint_name = tc.constraint_name \
                      WHERE constraint_type = 'FOREIGN KEY' AND tc.table_catalog='%s'" % database)
            fk_result = [row for row in cursor]
        return fk_result
        
    def table_column_names(self):
        with self.connect() as con:
            cursor = con.cursor()
            database = self.connection.database
            cursor.execute(
                "SELECT \
                tc.table_name, kcu.column_name \
                FROM \
                information_schema.table_constraints AS tc\
                JOIN information_schema.key_column_usage AS kcu \
                ON tc.constraint_name = kcu.constraint_name \
                WHERE constraint_type = 'PRIMARY KEY' AND tc.table_catalog='%s'" % database) 
            tbl_col_names = [row for row in cursor]
        return tbl_col_names

    def tables(self):
        with self.connect() as con:
            cursor = con.cursor()
            database = self.connection.database
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' \
                            AND table_type=\'BASE TABLE\' AND table_catalog='%s' AND table_name NOT LIKE \'\\_%%\'" % (database)) # to escape this sql command: ... NOT LIKE '\_%'
            tables = [table for (table,) in cursor]
        return tables

    def table_columns(self, table):
        with self.connect() as con:
            cursor = con.cursor()
            database = self.connection.database
            cursor.execute("SELECT column_name FROM information_schema.columns \
            WHERE table_name = '%s' AND table_catalog='%s'" % (table,database))
            columns = [col for (col,) in cursor]
        return columns

    def fmt_cols(self, cols):
        return ','.join(["%s" % col for col in cols])
    
    def fetch_types(self, table, cols):
        with self.connect() as con:
            cursor = con.cursor()
            types = {}
            cursor.execute("SELECT attname as col_name, atttypid::regtype AS base_type \
                        FROM pg_catalog.pg_attribute WHERE attrelid = 'public.%s'::regclass \
                        AND attnum > 0 AND NOT attisdropped ORDER  BY attnum;" % table)
            for rows in cursor:
                types[rows[0]] = rows[1]
        return types

    def fetch(self, table, cols):
        with self.connect() as con:
            cursor = con.cursor() 
            cursor.execute("SELECT %s FROM %s" % (self.fmt_cols(cols), table))
            result = [cols for cols in cursor]
        return result

    def select_where(self, table, cols, pk_att, pk):
        with self.connect() as con:
            cursor = con.cursor() 
            attributes = self.fmt_cols(cols)
            cursor.execute("SELECT %s FROM %s WHERE %s='%s'" % (attributes, table, att, val_att))
            result = [cols for cols in cursor]
        return result

    def column_values(self, table, col):
        with self.connect() as con:
            cursor = con.cursor()
            cursor.execute("SELECT DISTINCT %s, %s FROM %s" % (col, col, table))
            values = [val for (_,val) in cursor]
        return values
    
    def get_driver_name(self):
        return 'org.postgresql.Driver'

    def get_jdbc_prefix(self):
        return 'jdbc:postgresql://'
