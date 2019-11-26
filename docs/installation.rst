
Installation
============

The package was successfully installed on Linux, Windows and OS X systems.

Latest release from PyPI::

    pip install python-rdm

Latest from `GitHub <https://github.com/xflows/rdm/>`_::

    pip install https://github.com/xflows/rdm/archive/master.zip

The prerequisites are listed in ``requirements.txt``.

Prerequisites of specific ILP/RDM algorithms
--------------------------------------------

Depending on what algorithms you wish to use, these are their dependencies.

Aleph and RSD
^^^^^^^^^^^^^

* Yap prolog (preferably compiled with ``--tabling`` enabled for speedups). Check the Github repository `here <https://github.com/vscosta/yap-6.3>`_. Please use the latest version available. Old versions (older than 6.2) will likely not work.

On Debian-based systems you can simply install it as::

    apt install yap

TreeLiker, Caraf, Cardinalization, Quantiles, Relaggs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Java

1BC, 1BC2, Tertius
^^^^^^^^^^^^^^^^^^

These approaches depend on one original C program which must be compiled.
The sources are included with python-rdm in ``rdm/wrappers/tertius/src/``.

Documentation
-------------

You'll need Sphinx to build the documentation you are currently looking at::

    pip install -U Sphinx
