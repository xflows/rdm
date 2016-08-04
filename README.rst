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
   -  `Official page <http://ida.felk.cvut.cz/zelezny/rsd/index.htm>`__
   -  The source code is included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/rsd>`__
      (.pl files)
   -  Included with permission by the author

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
Lachiche <http://icube-sdc.unistra.fr/en/index.php/Nicolas_Lachiche>`__'s
team at the University of Strasbourg contributions:

-  **1BC, 1BC2, Tertius**

   -  By `Peter Flach <https://www.cs.bris.ac.uk/~flach/>`__ and
      `Nicolas
      Lachiche <http://icube-sdc.unistra.fr/en/index.php/Nicolas_Lachiche>`__
   -  Sources included here
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/tertius/src>`__
   -  Official sites:
      `Tertius <http://www.cs.bris.ac.uk/Research/MachineLearning/Tertius/index.html>`__,
      `1BC <http://www.cs.bris.ac.uk/Research/MachineLearning/1BC/index.html>`__
   -  Included with permission by the authors; please contact the
      authors for commercial use

-  **Caraf**

   -  By `Clement
      Charnay <http://icube-sdc.unistra.fr/en/index.php/Cl%C3%A9ment_Charnay>`__,
      `Agnès
      Braud <http://icube-sdc.unistra.fr/en/index.php/Agn%C3%A8s_Braud>`__
      and `Nicolas
      Lachiche <http://icube-sdc.unistra.fr/en/index.php/Nicolas_Lachiche>`__
      et al
   -  All implemented in the Caraf java binaries included
      `here <https://github.com/xflows/rdm/tree/master/rdm/wrappers/caraf/bin>`__
   -  Included with permission by the authors; please contact the
      authors for commercial use

-  **Relaggs** (Krogel and Wrobel, 2001), **Quantiles**,
   **Cardinalization**

   -  `Original Proper <http://www.cs.waikato.ac.nz/ml/proper/>`__
      adapted by `Nicolas
      Lachiche <http://icube-sdc.unistra.fr/en/index.php/Nicolas_Lachiche>`__
      et al
   -  GPLv2 license
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

Contributors to the RDM package code
------------------------------------

Anže Vavpetič (@anzev), Nicolas Lachiche, Alain Shakour (@alshak), Matic
Perovšek (@mperice)

-  `Knowldge Technologies Department <http://kt.ijs.si>`__, Jožef Stefan
   Institute, Ljubljana
-  `Engineering, Computer and Imaging Sciences
   Laboratory <http://icube-bfo.unistra.fr/en/index.php/Home>`__,
   University of Strasbourg, France

.. |Documentation Status| image:: https://readthedocs.org/projects/rdm/badge/?version=latest
   :target: http://rdm.readthedocs.io/en/latest/?badge=latest
