
Getting started
===============

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
    print theory

