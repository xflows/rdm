
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

This is a wrapper for the very popular ILP algorithm Aleph. Aleph is an ILP toolkit with many modes of
functionality: learning theories, feature construction, incremental learning, etc. Aleph uses mode
declarations to define the syntactic bias. Input relations are Prolog clauses, defined either extensionally
or intensionally.

`Official documentation <http://www.cs.ox.ac.uk/activities/machinelearning/Aleph/aleph>`_.

See :doc:`getting_started` for an example of using Aleph in your python code.

.. autoclass:: rdm.wrappers.Aleph
    :special-members:
    :members:

RSD
^^^

RSD is a relational subgroup discovery algorithm (Zelezny et al, 2001) composed of two main steps: the propositionalization step
    and the (optional) subgroup discovery step. RSD effectively produces an exhaustive list of first-order
    features that comply with the user-defined mode constraints, similar to those of
    Progol (Muggleton, 1995) and Aleph.

See :doc:`example` for an example of using RSD in your code.

.. autoclass:: rdm.wrappers.RSD
    :special-members:
    :members:

TreeLiker
^^^^^^^^^

TreeLiker (by Ondrej Kuzelka et al) is suite of multiple algorithms (controlled by the ``algorithm`` setting), RelF, Poly and HiFi:

*RelF* constructs a set of tree-like relational features by combining smaller conjunctive blocks.
The novelty is that RelF preserves the monotonicity of feature reducibility and redundancy
(instead of the typical monotonicity of frequency), which allows the algorithm to scale far
better than other state-of-the-art propositionalization algorithms.

*HiFi* is a propositionalization approach that constructs first-order features with hierarchical structure.
Due to this feature property, the algorithm performs the transformation in polynomial time of the maximum
feature length. Furthermore, the resulting features are the smallest in their semantic equivalence class.

`Official website <http://ida.felk.cvut.cz/treeliker/TreeLiker.html>`_

Example usage:

>>> context = DBContext(...)
>>> conv = TreeLikerConverter(context)
>>> treeliker = TreeLiker(conv.dataset(), conv.default_template())
>>> arff, _ = treeliker.run()

.. autoclass:: rdm.wrappers.TreeLiker
    :special-members:
    :members:

Wordification
^^^^^^^^^^^^^

Wordification (Perovsek et al, 2015) is a propositionalization method inspired by text mining that can be
viewed as a transformation of a relational database into a corpus of text documents. Wordification
constructs simple, easily interpretable features, acting as words in the transformed Bag-Of-Words
representation.

Example usage:

>>> context = DBContext(...)
>>> orange = OrangeConverter(context)
>>> wordification = Wordification(orange.target_Orange_table(), orange.other_Orange_tables(), context)
>>> wordification.run(1)
>>> wordification.calculate_weights()
>>> arff = wordification.to_arff()

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

This section documents helper utilities provided by the python-rdm package that are useful in
various scenarios.

Mapping unseen examples into propositional feature space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When testing classifiers (or in a real-world scenario) you'll need to map unseen (or new) examples into
the feature space used by the classifier. In order to do this, use the ``rdm.db.mapper`` function.

See :doc:`example` for usage in a cross-validation setting.

.. automodule:: rdm.db.mapper
    :members:


Validation
^^^^^^^^^^

Python-rdm provides a helper function for splitting a dataset into folds for cross-validation.

See :doc:`example` for a cross-validation example using RSD.

.. automodule:: rdm.validation
    :members:
