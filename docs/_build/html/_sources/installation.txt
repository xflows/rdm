
Installation
======================================

Prerequisites
-------------

* python >= 2.6
* mysql-connector-python (optionally, you can call the algorithms with their native input format)

Installing the Python-RDM package
---------------------------------

Latest release from PyPI::

    pip install python-rdm

Latest from GitHub::

    pip install https://github.com/anzev/rdm/archive/master.zip

Prerequisites of specific ILP/RDM algorithms
--------------------------------------------

Depending on what algorithms you wish to use, these are their dependencies.

Aleph and RSD
^^^^^^^^^^^^^

* yap prolog (preferably with ``--tabling`` enabled)

TreeLiker
^^^^^^^^^

* Java VM

Wordification
^^^^^^^^^^^^^

* orange 2.5 (this is planned to be dropped in favor of scikit-learn)


Documentation
-------------

You'll need Sphinx to build the documentation::
    
    pip install -U Sphinx
