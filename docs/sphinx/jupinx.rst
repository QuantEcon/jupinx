.. _jupinx:

Jupinx `cmd` line utility
=========================

.. contents::
    :depth: 1
    :local:

The `jupinx` command line utility.

.. note::

    this utility currently takes a zero-configuration approach. If you need
    to modify the behaviour of `sphinxcontrib-jupyter` then you need to update
    `conf.py` file in your sphinx project.

Installation 
------------

To install `jupinx`:

.. code-block:: bash

    pip install jupinx


to upgrade your current installation to the latest version:

.. code-block:: bash
    
    pip install jupinx --upgrade

Usage
-----

To build a collection of notebooks using `jupinx`:

.. code-block:: bash

    jupinx --notebooks <PATH-PROJECT-DIRECTORY>

or

.. code-block:: bash

    jupinx -n <PATH-PROJECT-DIRECTORY>

.. note::

    Many users will run `jupinx` at the root level of a repository.
    this can be done by specifying :code:`jupinx --notebooks`. The
    directory specification is optional in this case. 

It is also possible to build a full website. This option makes
use of Jupyter Notebooks ability to execute code so output is 
not required in any of the source files. The website can be 
completely built (including all code and generated components).

.. code-block:: bash

    jupinx --website <PATH-PROJECT-DIRECTORY>

.. note::

    There is currently **no** default template provided for constructing websites.
    This needs to be provided in the future to allow building websites out of
    the box with a default theme.

or 

.. code-block:: bash

    jupinx -w <PATH-PROJECT-DIRECTORY>

documentation regarding options for building websites can be found 
`here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-html.html>`__

All command line options available can be listed using the help flag:

.. code-block:: bash
    
    jupinx --help

or 

.. code-block:: bash

    jupinx -h

Options
-------

The typical usage for ``jupinx`` is:

.. code-block:: bash

    jupinx [OPTIONS] <DIRECTORY> [ADDITIONAL OPTIONS]

The following **options** are provided:

-h, --help            show this help message and exit
-c, --clean           clean build so sphinx recompiles all source documents
-j, --jupyterhub      open jupyter server when build completes to view notebooks
-n, --notebooks       compile a collection of Jupyter notebooks
                    [Result: _build/jupyter]
-s, --server          open html server when build completes to view website
-t, --coverage-tests  compile coverage report for project
                    [Result: <project-directory>/_build/coverage/reports/{filename}.json]
-w, --website         compile a website through Jupyter notebooks
                    [Result: _build/website/]
--version             show program's version number and exit

The following **additional options** are provided:

  -p [PARALLEL], --parallel [PARALLEL]
                        Specify the number of workers for parallel execution 
                        [Default: --parallel will result in --parallel=2 if no value is specified]
