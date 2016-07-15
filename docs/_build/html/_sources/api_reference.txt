
API Reference
======================================

The package is divided into two main independent subpackages: ``rdm.db`` and ``rdm.wrappers``.

Database interaction
--------------------

.. py:module:: rdm.db.datasource

Databases can be accessed via different so-called data sources. You can add your own data source by subclassing the base ``rdm.db.datasource.DataSource`` class.

Base DataSource
^^^^^^^^^^^^^^^

.. autoclass:: rdm.db.datasource.DataSource
    :special-members:
    :members:

MySQLDataSource
^^^^^^^^^^^^^^^ 

.. autoclass:: rdm.db.datasource.MySQLDataSource
    :special-members:
    :members:

.. py:module:: rdm.db.datasource

PgSQLDataSource
^^^^^^^^^^^^^^^

.. autoclass:: rdm.db.datasource.PgSQLDataSource
    :special-members:
    :members:

.. py:module:: rdm.db.context

Database Context
^^^^^^^^^^^^^^^^

A ``DBContext`` object represents a *view* of a particular data source that can be used for learning. Example uses include: selecting only particular tables, table columns, a target attribute, and so on.

.. autoclass:: rdm.db.context.DBContext
    :special-members:
    :members:

.. py:module:: rdm.db.converters

Database converters
-------------------

Converters are used to change the representation of the input database to a native representation of a particular algorithm.

.. autoclass:: rdm.db.converters.Converter
    :special-members:
    :members:

.. autoclass:: rdm.db.converters.ILPConverter
    :special-members:
    :members:

.. autoclass:: rdm.db.converters.RSDConverter
    :special-members:
    :members:

.. autoclass:: rdm.db.converters.AlephConverter
    :special-members:
    :members:

.. autoclass:: rdm.db.converters.OrangeConverter
    :special-members:
    :members:

.. autoclass:: rdm.db.converters.TreeLikerConverter
    :special-members:
    :members:

.. py:module:: rdm.wrappers

Algorithm wrappers
------------------

The ``rdm.wrappers`` module provides classes for working with the various algorithm wrappers.


Aleph
^^^^^

.. autoclass:: rdm.wrappers.Aleph
    :special-members:
    :members:

RSD
^^^

.. autoclass:: rdm.wrappers.RSD
    :special-members:
    :members:

TreeLiker
^^^^^^^^^

.. autoclass:: rdm.wrappers.TreeLiker
    :special-members:
    :members:

Wordification
^^^^^^^^^^^^^

.. autoclass:: rdm.wrappers.Wordification
    :special-members:
    :members:

Proper
^^^^^^

.. autoclass:: rdm.wrappers.Proper
    :special-members:
    :members:
    :undoc-members:

Tertius
^^^^^^^

.. autoclass:: rdm.wrappers.Tertius
    :special-members:
    :members:
    :undoc-members:

OneBC
^^^^^

.. autoclass:: rdm.wrappers.OneBC
    :special-members:
    :members:
    :undoc-members:

Caraf
^^^^^

.. autoclass:: rdm.wrappers.Caraf
    :special-members:
    :members:
    :undoc-members:


.. py:module:: rdm.validation


Utilities
---------


Mapping unseen examples into propositional feature space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: rdm.db.mapper
    :members:


Validation
^^^^^^^^^^

.. automodule:: rdm.validation
    :members:
