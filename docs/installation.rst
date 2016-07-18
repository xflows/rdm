
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

* Yap prolog (preferably compiled with ``--tabling`` enabled for speedups)

There are sources as well as binaries for Windows and OS X available `here <https://www.dcc.fc.up.pt/~vsc/Yap/downloads.html>`_.

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
