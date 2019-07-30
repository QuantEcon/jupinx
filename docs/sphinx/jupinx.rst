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

    jupinx --notebooks --directory <PATH>

.. note::

    Many users will run `jupinx` at the root level of a repository.
    this can be done by specifying :code:`jupinx --notebooks`. The
    directory specification is optional in this case. 

It is also possible to build a full website. This option makes
use of Jupyter Notebooks ability to execute code so output is 
not required in any of the source files. The website can be 
completely built (including all code and generated components).

.. code-block:: bash

    jupinx --website

documentation regarding options for building websites can be found 
`here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-html.html>`__

You can also see all command line options available using:

.. code-block:: bash
    
    jupinx --help


Options
-------

The following **build** options are provided:

-n, --notebooks     compile a set of Jupyter notebooks
                    [_build/jupyter]
-w, --website       compile notebooks and convert to HTML
                    [_build/website]
-c, --coverage      compile notebooks and run coverage tests
                    [_build/coverage]


Additional options can be provided:


-p, --parallel          request notebook execution and conversion 
                        to be processed in parallel. An integer 
                        may be specified to assign the number of 
                        dask workers. [**Default:** 2] 
                        *Example:* jupinx -w -p=4
-d, --directory         provide directory where Sphinx project is 
                        located. [**Default:** Current Working Directory]
                        *Example:* jupinx -n -d=repos/lecture-source-py/