
ClowdFlows
======================================

ClowdFlows is an open source web-based data mining platform. The python-rdm package 
also includes ClowdFlows widgets, which can be used to easily compose workflows
for mining relational databases.

User Documentation
^^^^^^^^^^^^^^^^^^^^^^^

Here's an example workflow that demonstrates the usage of RDM widgets in Clowdflows.
More specifically, the workflow constructs a decision tree on the Michalski Trains dataset (stored in a MySQL database) using Aleph to propositionalize the dataset.

.. figure:: images/aleph-mysql.PNG
    :target: http://clowdflows.org/workflow/2224/

    Click the image to open the ClowdFlows workflow.

* `Full ClowdFlows User docs <http://clowdflows-documentation.readthedocs.org/en/latest/user_doc_bycategory.html>`_
* `Public instance of ClowdFlows <http://clowdflows.com>`_

Developer Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can relatively easily extend your local ClowdFlows installation by developing new widgets. See the `Developer documentation <http://clowdflows-documentation.readthedocs.org/en/latest/cf_dev_wiki/dev-doc-home.html>`_ on ReadTheDocs.org, for instructions on how to develop and deploy widgets. 

You are of course welcome to share your widgets with everyone. To do so, please issue a pull request.

* `GitHub repository <https://github.com/janezkranjc/clowdflows>`_
* `Wiki <https://github.com/janezkranjc/clowdflows/wiki>`_
* `Developer documentation <http://clowdflows-documentation.readthedocs.org/en/latest/cf_dev_wiki/dev-doc-home.html>`_

The ``python-rdm`` ClowdFlows widgets follow the main ClowdFlows convention; ``rdm.db`` and ``rdm.wrappers`` can be imported as ClowdFlows packages and have the following internal structure:

* ``rdm/<package_name>`` - package root,
* ``rdm/<package_name>/package_data`` - widget database fixtures,
* ``rdm/<package_name>/static`` - widget-related static files, e.g., icons,
* ``rdm/<package_name>/library.py`` - main widget views,
* ``rdm/<package_name>/interaction_views.py`` - widget views that require a user interaction before doing a computation,
* ``rdm/<package_name>/visualization_views.py`` - widget views that visualize something after computation.
