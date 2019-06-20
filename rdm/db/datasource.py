from collections import defaultdict
#from exceptions import NotImplementedError
import mysql.connector as mysql

import re
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

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
            cursor.execute("SELECT %s FROM %s WHERE %s='%s'" % (attributes, table, pk_att, pk))
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


class SQLDataSource:
    '''
    A DataSource implementation for accessing datasets from a PosgreSQL DBMS.
    '''
    def __init__(self, connection):
        '''
            :param connection: a DBConnection instance.
        '''
        self.connection = connection

        variable_types_file = open("variable_types.txt")
        variable_types = [line.strip().lower() for line in variable_types_file.readlines()]
        variable_types_file.close()

        table_trigger = False
        table_header = False
        current_table = None
        sqt = defaultdict(list)
        tabu = ["KEY","PRIMARY","CONSTRAINT"]
        table_keys = defaultdict(list)
        primary_keys = {}
        foreign_key_graph = []
        variable_types_dict = defaultdict(defaultdict)
        fill_table=False
        tables = dict()
        with open (connection.database,"r") as sqf:
            for line in sqf:
                if "INSERT INTO" in line:
                    table_header=False
                    vals = line.strip().split()
                    vals_real = " ".join(vals[4:]).split("),(")
                    vals_real[0] = vals_real[0].replace("(","")
                    vals_real[len(vals_real)-1] = vals_real[len(vals_real)-1].replace(");","")
                    col_num = len(sqt[current_table])
                    vx = []
                    for x in vals_real:
                        values = re.split(r",(?=(?:[^\']*\'[^\']*\')*[^\']*$)", x)
                        if len(values) == col_num:
                            new_values = []
                            for value in values:
                                if value == "NULL":
                                    value = value
                                elif (value[0] == "'" and value[-1] == "'") or (value[0] == '"' and value[-1] == '"'):
                                    value = value[1:-1]
                                else:
                                    if ("." in value) or ("," in value):
                                        value = float(value)
                                    else:
                                        value = int(value)
                                new_values.append(value)
                            vx.append(new_values)
                    dfx = pd.DataFrame(vx)
                    try:
                        assert dfx.shape[1] == len(sqt[current_table])
                    except:
                        print(sqt[current_table])
                        print(col_num,re.split(r",(?=(?:[^\']*\'[^\']*\')*[^\']*$)", vals_real[0]))

                    dfx.columns = [clear(x) for x in sqt[current_table]]
                    tables[current_table] = dfx
                if table_trigger and table_header:
                    line = line.strip().split()
                    if len(line) > 0:
                        if line[0] not in tabu:
                            if line[0] != "--":
                                variable_type = re.sub(r'\([^)]*\)', '', line[1])
                                if variable_type.lower() in variable_types:
                                    variable_types_dict[current_table][clear(line[0])] = variable_type
                                    sqt[current_table].append(clear(line[0]))
                        else:
                            if line[0] == "KEY":
                                table_keys[current_table].append(clear(line[2]))
                            if line[0] == "PRIMARY":
                                primary_keys[current_table] = cleanp(clear(line[2]))
                                table_keys[current_table].append(clear(line[2]))
                            if line[0] == "CONSTRAINT":
                                # t1 a1 t2 a2
                                foreign_key_quadruplet = [clear(cleanp(x)) for x in [current_table,line[4],line[6],line[7]]]
                                foreign_key_graph.append(foreign_key_quadruplet)

                if "CREATE TABLE" in line:
                    table_trigger = True
                    table_header = True
                    current_table = clear(line.strip().split(" ")[2])

        self.source_data = {"tables": tables, "fkgs": foreign_key_graph, "primary_keys": primary_keys, "variable_types": variable_types_dict}

    def connected(self,tables,cols,find_connections):

        fkgs = self.source_data["fkgs"]
        primary_keys = self.source_data["primary_keys"]

        context = {}
        context["connected"] = defaultdict(list)
        context["fkeys"] = defaultdict(set)
        context["reverse_fkeys"] = defaultdict(set)
        connected = defaultdict(set)

        for fkg in fkgs:
            connected[(fkg[0],fkg[2])].add((fkg[1], fkg[3]))
            connected[(fkg[2],fkg[0])].add((fkg[3], fkg[1]))
            if not(fkg[1] in primary_keys[fkg[0]]):
                context["fkeys"][fkg[0]].add(fkg[1])
                context["reverse_fkeys"][(fkg[0],fkg[1])].add(fkg[2])

        for connection in connected:
            context["connected"][connection] = list(connected[connection])

        return context["connected"], primary_keys, context["fkeys"], context["reverse_fkeys"]

    def foreign_keys(self):
        return [tuple(fkg) for fkg in self.source_data["fkgs"]]

    def table_column_names(self):
        table_col_names = []
        for key in self.source_data["primary_keys"]:
            table_col_names.append((key,self.source_data["primary_keys"][key]))
        return table_col_names

    def tables(self):
        return [table for table in self.source_data["tables"]]

    def table_columns(self, table):
        return list(self.source_data["tables"][table].columns.values)

    def fmt_cols(self, cols):
        return ','.join(["%s" % col for col in cols])

    def fetch_types(self, table, cols):
        var_types = {}
        for key in self.source_data["variable_types"][table]:
            if key in cols:
                var_types[key] = self.source_data["variable_types"][table][key]
        return var_types

    def fetch(self, table, cols):
        return [tuple(x) for x in self.source_data["tables"][table][cols].values]

    def select_where(self, table, cols, pk_att, pk):
        return [tuple(x) for x in self.source_data["tables"][table].loc[self.source_data["tables"][table][pk_att] == pk][cols].values]

    def column_values(self, table, col):
        return list(self.source_data["tables"][table][col].unique())


    def get_driver_name(self):
        raise NotImplementedError()

    def get_jdbc_prefix(self):
        raise NotImplementedError()

def cleanp(stx):
    return stx.replace("(","").replace(")","").replace(",","")

def clear(stx):
    return stx.replace("`","").replace("`","")
