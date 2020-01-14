from rdm.db import DBContext, AlephConverter, SQLiteDBConnection
from rdm.wrappers import Aleph

# Connect to the database
connection = SQLiteDBConnection('data/trains/trains.sqlite3')

# Define learning context
context = DBContext(connection, target_table='trains', target_att='direction')

# Convert the data and induce features using Aleph
conv = AlephConverter(context, target_att_val='east')
aleph = Aleph()
theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                conv.negative_examples(),
                                conv.background_knowledge())
print(theory)
