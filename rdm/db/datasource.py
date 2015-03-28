from exceptions import NotImplementedError


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


    def connections(self):
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
