from collections import defaultdict
from exceptions import NotImplementedError
import mysql.connector as sql


class DataSource:
    '''
    A data abstraction layer for accessing datasets.
    '''
    def tables(self):
        '''
        Returns a list of table names.
        '''
        raise NotImplementedError()


    def table_columns(self, table_name):
        '''
        Returns a list of columns for the given table.
        '''
        raise NotImplementedError()


    def connected(self):
        '''
        Returns a list of tuples of connected table pairs.
        '''
        raise NotImplementedError()


    def table_primary_key(self, table_name):
        '''
        Returns the primary key attribute name for the given table.
        '''
        raise NotImplementedError()


    def fetch(self, table, cols):
        '''
        Fetches rows for the given table and columns.
        '''
        raise NotImplementedError()


    def select_where(self, table, cols, pk_att, pk):
        '''
        Select with where clause.
        '''
        raise NotImplementedError()


    def fetch_types(self, table, cols):
        '''
        Returns a dictionary of field types for the given table and columns.
        '''
        raise NotImplementedError()


    def column_values(self, table, col):
        '''
        Returns a list of distinct values for the given table and column.
        '''
        raise NotImplementedError()


class MySQLDataSource(DataSource):
    
    def __init__(self, connection):
        '''
        @connection: a DBConnection instance.
        '''
        self.connection = connection


    def tables(self):
        with self.connection.connect() as con:
            cursor = con.cursor()
            cursor.execute('SHOW tables')
            tables = [table for (table,) in cursor]
        return tables


    def table_columns(self, table_name):
        with self.connection.connect() as con:
            cursor = con.cursor()
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '%s' AND table_schema='%s'" % (table_name, self.connection.database))
            columns = [col for (col,) in cursor]
        return columns


    def connected(self, tables, cols, find_connections=False):
        connected = defaultdict(list)
        fkeys = defaultdict(set)
        reverse_fkeys = {}
        pkeys = {}
        with self.connection.connect() as con:
            cursor = con.cursor()
            cursor.execute(
               "SELECT table_name, column_name, referenced_table_name, referenced_column_name \
                FROM information_schema.KEY_COLUMN_USAGE \
                WHERE referenced_table_name IS NOT NULL AND table_schema='%s'" % self.connection.database)
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
            for (table, col, ref_table, ref_col) in cursor:
                connected[(table, ref_table)].append((col, ref_col))
                connected[(ref_table, table)].append((ref_col, col))
                fkeys[table].add(col)
                reverse_fkeys[(table, col)] = ref_table

            cursor.execute(
                "SELECT table_name, column_name \
                 FROM information_schema.KEY_COLUMN_USAGE \
                 WHERE constraint_name='PRIMARY' AND table_schema='%s'" % self.connection.database)
            for (table, pk) in cursor:
                pkeys[table] = pk

        return connected, pkeys, fkeys, reverse_fkeys


    def fmt_cols(self, cols):
        return ','.join(["`%s`" % col for col in cols])


    def fetch(self, table, cols):
        with self.connection.connect() as con:
            cursor = con.cursor() 
            cursor.execute("SELECT %s FROM %s" % (self.fmt_cols(cols), table))
            result = [cols for cols in cursor]
        return result


    def select_where(self, table, cols, pk_att, pk):
        with self.connection.connect() as con:
            cursor = con.cursor() 
            attributes = self.fmt_cols(cols)
            cursor.execute("SELECT %s FROM %s WHERE `%s`='%s'" % (attributes, table, pk_att, pk))
            result = [cols for cols in cursor]
        return result


    def fetch_types(self, table, cols):
        with self.connection.connect() as con:
            cursor = con.cursor() 
            cursor.execute("SELECT %s FROM `%s` LIMIT 1" % (self.fmt_cols(cols), table))
            cursor.fetchall()
            types = {}
            for desc in cursor.description:
                types[desc[0]] = sql.FieldType.get_info(desc[1])
        return types


    def column_values(self, table, col):
        with self.connection.connect() as con:
            cursor = con.cursor()
            cursor.execute("SELECT DISTINCT BINARY `%s`, `%s` FROM `%s`" % (col, col, table))
            values = [val for (_,val) in cursor]
        return values
