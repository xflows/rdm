
Getting started
===============

Using csv files
---------------

Here is a simple example which loads the famous `East-West challenge dataset (trains) <https://relational.fit.cvut.cz/dataset/Trains>`_ from two .csv files using :class:`~rdm.db.context.CSVConnection`. CSV files must contain two additional header lines beside column names which specify data types using SQLite syntax, and constraints such as primary and foreign key using simplified SQLite syntax. The


.. csv-table:: :download:`trains.csv <../examples/data/trains/trains.csv>`
   :header: "id", "direction"
   :widths: 15, 15

   integer,varchar
   primary key,
   1,east
   2,east
   ...,...
   19,west
   20,west


.. csv-table:: :download:`cars.csv <../examples/data/trains/cars.csv>`
  :header: id,tid,position,shape,len,sides,roof,wheels,load_shape,load_num
  :widths: 15,15,15,15,15,15,15,15,15,15

  integer,integer,integer,varchar,varchar,varchar,varchar,integer,varchar,integer
  primary key,foreign key [trains.id],,,,,,,,
  1,1,1,rectangle,short,not_double,none,2,circle,1
  2,1,2,rectangle,long,not_double,none,3,hexagon,1
  3,1,3,rectangle,short,not_double,peaked,2,triangle,1
  ...,...,...,...,...,...,...,...,...,...
  62,20,1,rectangle,long,not_double,flat,3,hexagon,1
  63,20,2,u_shaped,short,not_double,none,2,triangle,1



.. code:: python

    from rdm.db import DBVendor, DBContext, AlephConverter, SQLiteDBConnection, CSVConnection
    from rdm.wrappers import Aleph

    # Provide data
    connection = CSVConnection(['examples/data/trains/trains.csv',
                                 'examples/data/trains/cars.csv'])

    # Define learning context
    context = DBContext(connection, target_table='trains', target_att='direction')

    # Convert the data and induce features using Aleph
    conv = AlephConverter(context, target_att_val='east')
    aleph = Aleph()
    theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                    conv.negative_examples(),
                                    conv.background_knowledge())
    print(theory)


Using SQLite
------------

If the third line of the code above is changed as shown below the SQLite database containing the same data will be used.

.. code:: python

    connection = SQLiteDBConnection('examples/data/trains/trains.sqlite3')




Using MySQL
-----------

The same example but the data is now loaded from a MySQL database using :class:`~rdm.db.context.DBConnection`.


.. code:: python

    from rdm.db import DBVendor, DBConnection, DBContext, AlephConverter
    from rdm.wrappers import Aleph

    # Provide connection information
    connection = DBConnection(
        'ilp',             # User
        'ilp123',          # Password
        'workflow.ijs.si', # Host
        'ilp',             # Database
    )

    # Define learning context
    context = DBContext(connection, target_table='trains', target_att='direction')

    # Convert the data and induce features using Aleph
    conv = AlephConverter(context, target_att_val='east')
    aleph = Aleph()
    theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                    conv.negative_examples(),
                                    conv.background_knowledge())
    print(theory)
