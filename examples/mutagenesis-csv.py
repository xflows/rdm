from rdm.db import DBContext, AlephConverter, CSVConnection
from rdm.wrappers import Aleph


# Load data from a set of csv files
connection = CSVConnection(['data/mutagenesis42/atoms.csv',
                            'data/mutagenesis42/bonds.csv',
                            'data/mutagenesis42/drugs.csv',
                            'data/mutagenesis42/ring_atom.csv',
                            'data/mutagenesis42/ring_strucs.csv',
                            'data/mutagenesis42/rings.csv'
                            ])

# Define learning context
context = DBContext(connection, target_table='atoms', target_att='element')

# Convert the data and induce features using Aleph
conv = AlephConverter(context, target_att_val='c')

aleph = Aleph()
theory, features = aleph.induce('induce_features', conv.positive_examples(),
                                conv.negative_examples(),
                                conv.background_knowledge())
print(theory)
print(features)
