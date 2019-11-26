from rdm.db import DBContext, AlephConverter, SQLiteDBConnection
from rdm.wrappers import Aleph

# Connect to a database
connection = SQLiteDBConnection('data/mutagenesis42/mutagenesis42.sqlite3')

# Define learning context
context = DBContext(connection, target_table='atoms', target_att='element')

# Convert the data and induce features using Aleph
conv = AlephConverter(context, target_att_val='c')
aleph = Aleph()
theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                conv.negative_examples(),
                                conv.background_knowledge())
print(theory)
