Python Relational Data Mining
=============================

|Documentation Status|

This python project was created to enable easier use of several
inductive logic programming (ILP) and relational data mining (RDM)
algorithm implementations. One important aim of the project is to offer
a common bridge between a RDBMS and the ILP&RDM implementations, since
many of approaches accept databases in their own format.

This project also includes the UI components (widgets) for the
`ClowdFlows <https://github.com/xflows/clowdflows/>`__ data mining
platform.

Currently, the project offers support for MySQL and PostgreSQL databases
and the following algorithms: Aleph, RSD, Wordification, TreeLiker,
Caraf, Relaggs, Quantiles, Cardinalization, 1BC, 1BC2, and Tertius.

Included approaches
-------------------

Although python-rdm itself is MIT licensed, we include approaches that
have their own licenses (all of the sources are unmodified). To be sure,
please contact the respective authors if you want to use their approach
for any commercial purposes.

-  **Aleph**

   -  `Official
      page <http://www.cs.ox.ac.uk/activities/machinelearning/Aleph/aleph>`__
   -  Freely available for academic purposes, contact the author `Ashwin
      Srinivasan <http://www.cse.iitd.ernet.in/~ashwin/work/index.html>`__
      for commercial use
   -  The source code is included
      `here <https://github.com/xflows/rdm/blob/master/rdm/wrappers/aleph/>`__
      (aleph.pl)

-  **RSD**

   -  by `Filip Železný <ida.felk.cvut.cz/zelezny/>`__ et al
   -  The source code is included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/rsd>`__
      (.pl files)

-  **TreeLiker** (includes HiFi, RelF and Poly)

   -  `Official
      page <http://ida.felk.cvut.cz/treeliker/TreeLiker.html>`__
   -  The binaries are included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/treeliker/bin/>`__
   -  GPL license

-  **Wordification**

   -  by `Matic Perovšek <mailto:matic.perovsek@ijs.si>`__ et al
   -  python-rdm is currently the main repository for this approach.
   -  The source code is included
      `here <https://github.com/xflows/rdm/blob/master/rdm/wrappers/wordification/>`__
   -  MIT license

`Nicolas
Lachiche <http://icube-bfo.unistra.fr/index.php/Nicolas_Lachiche>`__'s
team at the University of Strassbourg contributions:

-  **1BC, 1BC2, Tertius**

   -  By `Peter Flach <https://www.cs.bris.ac.uk/~flach/>`__ and
      `Nicolas
      Lachiche <http://icube-bfo.unistra.fr/index.php/Nicolas_Lachiche>`__
   -  Sources included here
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/tertius/src>`__

-  **Caraf**

   -  By `Nicolas
      Lachiche <http://icube-bfo.unistra.fr/index.php/Nicolas_Lachiche>`__
      et al
   -  All implemented in the Caraf java binaries included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/caraf/bin>`__

-  **Relaggs** (Krogel and Wrobel, 2001), **Quantiles**,
   **Cardinalization**

   -  By `Nicolas
      Lachiche <http://icube-bfo.unistra.fr/index.php/Nicolas_Lachiche>`__
      et al
   -  All implemented in the Proper java binaries included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/proper/bin>`__

Installation, documentation
---------------------------

Please find installation instructions, examples and API reference on
`Read the Docs <http://rdm.readthedocs.org/en/latest/>`__.

Note
----

Please note that this is a research project and that drastic changes can
be (and are) made pretty regularly. Changes are documented in the
`CHANGELOG <CHANGELOG.md>`__.

Pull requests and issues are welcome.

Contributors
------------

Anže Vavpetič (@anzev), Nicolas Lachiche, Alain Shakour (@alshak), Matic
Perovšek (@mperice)

-  `Knowldge Technologies Department <http://kt.ijs.si>`__, Jožef Stefan
   Institute, Ljubljana
-  `Engineering, Computer and Imaging Sciences
   Laboratory <http://icube-bfo.unistra.fr/en/index.php/Home>`__,
   University of Strasbourg, France

.. |Documentation Status| image:: https://readthedocs.org/projects/rdm/badge/?version=latest
   :target: http://rdm.readthedocs.io/en/latest/?badge=latest
