# Python Relational Data Mining #

This python project was created to enable easier use of several inductive logic programming (ILP) and relational data mining (RDM)
algorithm implementations. One important aim of the project is to offer a common bridge between a RDBMS and the ILP&RDM implementations, since many of approaches accept databases in their own format.

This project also includes the UI components (widgets) for the [ClowdFlows](https://github.com/janezkranjc/clowdflows/) data mining platform.

<!-- TODO: add citations, licenses --> 
Currently, the project offers support for MySQL and PostgreSQL databases and the following algorithms: Aleph, RSD, Wordification, TreeLiker, Relaggs, Quantiles, Cardinalization, 1BC, 1BC2, and Tertius.

## Work in progress ##

* This project was previously part of the ClowdFlows codebase and is now in the process of becoming a standalone project. 
* Droping orange to use scikit-learn instead.
* Adding support for other RDBMSs.

## Docs ##

The documentation is available on [Read the Docs](http://rdm.readthedocs.org/en/latest/) (work in progress).

## Prerequisites ##

* python >= 2.6
* mysql-connector-python
* orange 2.5

Depending on what algorithms you plan to use, these are the specific requirements for each.

### Aleph, RSD: ###
* yap prolog (preferably with --tabling enabled)

### TreeLiker, Relaggs, Quantiles, Cardinalization ###
* Java VM

### Wordification ###
* Only the basic package prerequisites

### 1BC, 1BC2, Tertius ###

1BC, 1BC2 and Tertius need to be compiled with the makefile found in workflows/ilp/tertius/src. The goals are "1BC" and "tertius". 1BC and 1BC2 are compiled with the same goal. The executable files need to be moved to workflows/ilp/tertius/bin.

## Note ##

Please note that this is a research project and that drastic changes can be (and are) made pretty regularly. Changes are documented in the [CHANGELOG](CHANGELOG.md).

Pull requests and issues are welcome.

## Contributors ##

Anže Vavpetič (@anzev), Alain Shakour (@alshak), Matic Perovšek (@mperice)

* [Knowldge Technologies Department](http://kt.ijs.si), Jožef Stefan Institute, Ljubljana
* [Engineering, Computer and Imaging Sciences Laboratory](http://icube-bfo.unistra.fr/en/index.php/Home), University of Strasbourg, France
