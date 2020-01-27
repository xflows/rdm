from collections import defaultdict
import pprint
import copy
import socket
import sqlite3
import tempfile
import os
import csv
import re
import sys

import pymysql as mysql
import psycopg2 as postgresql
from .converters import OrangeConverter

from .datasource import MySQLDataSource, PgSQLDataSource, SQLiteDataSource


def is_open(host, port, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    status = True
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RDWR)
    except:
        status = False
    finally:
        s.close()
        return status


class DBVendor:
    MySQL = 'mysql'
    PostgreSQL = 'postgresql'
    SQLite = 'sqlite'
    CSV = 'csv'


class DBConnection:
    '''
    Database connector with credentials and database settings
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
        self.port = None

        if self.vendor == DBVendor.MySQL:
            self.src = MySQLDataSource(self)
            self.port = 3306
        elif self.vendor == DBVendor.PostgreSQL:
            self.src = PgSQLDataSource(self)
            self.port = 5432
        else:
            raise Exception("Unknown DB vendor: {}".format(vendor))

        self.check_port()
        self.check_connection()

    def check_port(self):
        if not is_open(self.host, self.port):
            raise Exception('Port {} is not open on host {}'.format(self.port, self.host))

    def check_connection(self):
        try:
            with self.connect() as _:
                pass
        except Exception as e:
            raise Exception('Problem connecting to the database. Please re-check your credentials.')

    def connection(self):
        return self.connect().con

    def connect(self):
        dal_connect_fun = None
        if self.vendor == DBVendor.MySQL:
            dal_connect_fun = mysql.connect
        elif self.vendor == DBVendor.PostgreSQL:
            dal_connect_fun = postgresql.connect

        if not dal_connect_fun:
            raise Exception('Unsupported or unset database vendor: {}'.format(dal_connect_fun))

        return DBConnection.Manager(self.user, self.password, self.host, self.database, dal_connect_fun)


class SQLiteDBConnection(DBConnection):
    '''
    SQLite database connector
    '''

    class Manager:
        '''
        Context Manager.
        '''

        def __init__(self, sqlite_database, dal_connect_fun):
            self.con = dal_connect_fun(sqlite_database)

        def __enter__(self):
            return self.con

        def __exit__(self, exc_type, exc_value, traceback):
            self.con.close()

    def __init__(self, sqlite_database, vendor=DBVendor.SQLite):
        self.sqlite_database = sqlite_database
        self.src = SQLiteDataSource(self)
        if not(sqlite3.sqlite_version_info[0] >= 3 and sqlite3.sqlite_version_info[1] >= 16):
            raise Exception('Your SQLite does not support pragma functions. Please upgrade to at least 3.16.0')
        self.check_connection()

    def connect(self):
        return self.Manager(self.sqlite_database, sqlite3.connect)

    def check_port(self):
        pass


class CSVConnection(SQLiteDBConnection):
    '''
    CSV data loader. An SQLite database is used internally to store and query the data.
    Input csv files require two additional header lines besides the title row:

    - the first row specifies column names
    - the second row specifies column types using SQLite syntax
    - the third row specifies constraints such as primary and foreign keys using simplified SQLite syntax:

        - **primary key** declares a primary key constraint on the given column
        - **foreign key [table.column]** declares a foreign key constraint on the current column to the specified table and column. See notes below for additional information.


    **Notes**

    Composite primary keys are supported simply by declaring several colums as "primary key".
    Both primary and foreign key can be declared in a single csv cell. For example, "primary key foreign key [table.column]" is a valid declaration (although not very useful if the primary key is not composite because it implies one-to-one relationship).

    If there are multiple foreign key declarations per cell only the first one is considered and the rest is discarded (such declaration is invalid anyway).

    Finally, composite foreign keys are not (yet) supported because there is no simple way of expressing such constraints in the csv header.
    '''
    def __init__(self, file_list):
        self.sqlite_database = os.path.join(tempfile.mkdtemp(), 'tempdb.sqlite3')
        self.__csv2db(file_list)
        self.src = SQLiteDataSource(self)
        if not(sqlite3.sqlite_version_info[0] >= 3 and sqlite3.sqlite_version_info[1] >= 16):
            raise Exception('Your SQLite does not support pragma functions. Please upgrade to at least 3.16.0')
        self.check_connection()

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.

        # Now store a dump of the db file. This is required for unpickled instance to work.
        self.dbdump = open(self.sqlite_database, 'rb').read()
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['src']
        del state['sqlite_database']
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.__dict__.update(state)
        sqldb = os.path.join(tempfile.mkdtemp(), 'tempdb.sqlite3')
        with open(sqldb, 'wb') as fp:
            fp.write(self.dbdump)
        src = SQLiteDataSource(self)
        self.sqlite_database = sqldb
        self.src = src

    def __del__(self):
        try:
            tmpdir, _ = os.path.split(self.sqlite_database)
            if os.path.exists(self.sqlite_database):
                os.remove(self.sqlite_database)
                os.rmdir(tmpdir)
        except Exception as e:
            print('Warning: cannot remove temporary database "{}"'.format(self.sqlite_database))

    def connect(self):
        return self.Manager(self.sqlite_database, sqlite3.connect)

    def __csv2db(self, file_list):
        '''
        Loads csv files into an SQLite database and checks foreign keys constraints
        '''
        with sqlite3.connect(self.sqlite_database) as conn:
            for fname in file_list:
                ddl, insert, data = self.csv2sql(fname)
                # print(fname)
                # print(ddl)
                # print(insert)
                # print(data[0])
                # print('\n')
                conn.execute("PRAGMA foreign_keys = 0")
                conn.executescript(ddl)
                conn.commit()
                conn.executemany(insert, data)
                conn.commit()
            conn.execute('PRAGMA foreign_keys = 1')
            errors = list(conn.execute('PRAGMA foreign_key_check'))
            if errors:
                errlines = ['table "{}", row {}'.format(row[0], row[1]) for row in errors]
                raise ValueError('Foreign key constraint error:\n{}'.format('\n'.join(errlines)))

    def csv2sql(self, fname):
        '''
        Parses csv data file and returns SQLite DDL, insert command and data rows.
        '''
        tablename = os.path.splitext(os.path.split(fname)[1])[0]
        data = []
        with open(fname) as fp:
            reader = csv.reader(fp)
            columns, types, keys = next(reader), next(reader), next(reader)
            columns = [x.strip() for x in columns]
            types = [x.strip() for x in types]
            keys = [x.strip() for x in keys]

            if len(set([len(columns), len(types), len(keys)])) != 1:
                raise SyntaxError('Invalid header lines 1-3 in "{}": not the same length'.format(fname))

            declarations = []
            constraints = []
            pkeys = []
            # this can parse complex declarations such as "primary key foreign key [table.col]"
            for name, typ, key in zip(columns, types, keys):
                if not key:
                    declarations.append('"{}" {}'.format(name, typ))
                else:
                    found = re.search('primary[ ]+key[ ]*', key, flags=re.IGNORECASE)
                    added = False
                    if found:
                        pkeys.append(name)
                        declarations.append('"{}" {}'.format(name, typ))
                        added = True
                        key = re.sub('[ ]*primary[ ]+key[ ]*', '', key, flags=re.IGNORECASE)

                    found = re.search('foreign[ ]+key[ ]*\[[^\[]+\]', key, flags=re.IGNORECASE)
                    if found:
                        if not added:
                            declarations.append('"{}" {}'.format(name, typ))
                        fkref = found.group(0)  # only the first declaration, ignore the rest because it is invalid
                        fkref = re.sub('[ ]*foreign[ ]+key[ ]*', '', fkref, flags=re.IGNORECASE).strip()
                        fkref = fkref.replace('[', '').replace(']', '').strip()
                        try:
                            ftable, fcol = fkref.split('.')
                        except:
                            raise SyntaxError('Invalid FOREIGN KEY declaration: "{}"'.format(found.group(0)))
                        constraints.append('FOREIGN KEY("{}") REFERENCES "{}"("{}")'.format(name, ftable, fcol))
            data = list(reader)
        if len(pkeys) == 0:
            raise ValueError('No primary key is defined in file "{}"'.format(fname))
        constraints.append('PRIMARY KEY ({})'.format(','.join(['"{}"'.format(x) for x in pkeys])))

        ddl = 'CREATE TABLE "{}" (\n{}\n)'.format(tablename, ',\n'.join(declarations + constraints))
        insert = 'INSERT INTO "{}" VALUES ({})'.format(tablename, ','.join('?' * len(declarations)))
        return ddl, insert, data

    def dump_sql(self, sqlfile):
        '''
        Dumps the database contructed from csv files into an SQLite SQL file

            :param sqlfile: name of the output file
        '''
        with open(sqlfile, 'w') as fp:
            with sqlite3.connect(self.sqlite_database) as con:
                for line in con.iterdump():
                    fp.write('{}\n'.format(line))

    def dump_db(self, sqlite_database_file):
        '''
        Dumps the database constructed from csv files into an SQLite database file.

        Python 3.7 and SQLite 3.6.11 or newer are required to use this function.
        '''
        if not(sys.version_info.major >= 3 and sys.version_info.minor >= 7):
            raise EnvironmentError('Python >= 3.7 and SQLite >= 3.6.11 are required for backuping SQLite databases')
        with sqlite3.connect(self.sqlite_database) as con:
            with sqlite3.connect(sqlite_database_file) as bck:
                con.backup(bck, pages=0)


class DBContext:
    def __init__(self, connection, target_table=None, target_att=None,
                 find_connections=False, in_memory=True):
        '''
            Initializes a new DBContext object from the given DBConnection.

            :param connection: a DBConnection instance
            :param target_table: set a target table for learning
            :param target_att: set a target table attribute for learning
            :param find_connections: set to True if you want to detect relationships based on attribute and table names, \
             e.g., ``train_id`` is the foreign key refering to ``id`` in table ``train``.
            :param in_memory: Load the database into main memory (currently required for most approaches and pre-processing)
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

        self.target_table = self.tables[0] if not target_table else target_table
        self.target_att = None if not target_att else target_att

        self.orng_tables = None
        self.in_memory = in_memory

        if in_memory:
            self.orng_tables = self.read_into_orange()

    def read_into_orange(self):
        conv = OrangeConverter(self)
        tables = {
            self.target_table: conv.target_Orange_table()
        }
        other_tbl_names = [table for table in self.tables if table != self.target_table]
        other_tables = dict(list(zip(other_tbl_names, conv.other_Orange_tables())))
        tables.update(other_tables)
        return tables

    def fetch(self, table, cols):
        '''
        Fetches rows from the db.

            :param table: table name to select
            :cols: list of columns to select
            :return: list of rows
            :rtype: list
        '''
        return self.src.fetch(table, cols)

    def rows(self, table, cols):
        '''
        Fetches rows from the local cache or from the db if there's no cache.

            :param table: table name to select
            :cols: list of columns to select
            :return: list of rows
            :rtype: list
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

            :param table: target table
            :param cols: list of columns to select
            :param pk_att: attribute for the where clause
            :param pk: the id that the pk_att should match
            :return: rows from the given table and cols, with the condition pk_att==pk
            :rtype: list
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

            :param table: target table
            :param cols: list of columns to select
            :return: a dictionary of types for each attribute
            :rtype: dict
        '''
        return self.src.fetch_types(table, cols)

    def compute_col_vals(self):
        for table, cols in list(self.cols.items()):
            self.col_vals[table] = {}
            for col in cols:
                self.col_vals[table][col] = self.src.column_values(table, col)

    def copy(self):
        '''
        Makes a deepcopy of the DBContext object (e.g., for making folds)

            :returns: a deep copy of ``self``.
            :rtype: DBContext
        '''
        return copy.deepcopy(self)

    def __repr__(self):
        return pprint.pformat({
            'target_table': self.target_table,
            'target attribute': self.target_att,
            'tables': self.tables,
            'cols': self.cols,
            'connected': self.connected,
            'pkeys': self.pkeys,
            'fkeys': self.fkeys,
            'orng_tables': [(name, len(table)) for name, table in
                            list(self.orng_tables.items())] if self.orng_tables else 'not in memory'
        })
