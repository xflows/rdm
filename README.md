# Python Relational Data Mining #

This python project was created to enable easier use of several inductive logic programming (ILP) and relational data mining (RDM)
algorithm implementations. One important aim of the project is to offer a common bridge between a RDBMS and the ILP&RDM implementations, since many of approaches accept databases in their own format.

This project also includes the UI components (widgets) for the [ClowdFlows](https://github.com/janezkranjc/clowdflows/) data mining platform.

<!-- TODO: add citations, licenses --> 
Currently, the project offers support for MySQL databases and the following algorithms: Aleph, RSD, Wordification, and TreeLiker.

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

### TreeLiker ###
* Java VM

### Wordification ###
* Only the basic package prerequisites

## Note ##

Please note that this is a research project and that drastic changes can be (and are) made pretty regularly. Changes are documented in the [CHANGELOG](CHANGELOG.md).

Pull requests and issues are welcome.
