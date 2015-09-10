
Getting started
======================================

.. code:: python

  # Provide connection information
  connection = DBConnection(
      'ilp',             # User
      'ilp123',          # Password
      'workflow.ijs.si', # Host
      'ilp'              # Database
  )
  data_source = MySQLDataSource(connection)

  # Define learning context
  context = DBContext(data_source)
  context.target_table = 'trains'
  context.target_att = 'direction'

  # Convert the data and induce features using Aleph
  conv = AlephConverter(context, target_att_val = 'east')
  aleph = Aleph()
  theory, features = aleph.induce('induce_features', conv.positive_examples(), 
                                  conv.negative_examples(),
                                  conv.background_knowledge())
  print theory
