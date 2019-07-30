.. _jupinx:

Jupinx `cmd` line utility
=========================

The `jupinx` command line utility.

.. note::

    this utility currently takes a zero-configuration approach. If you need
    to modify the behaviour of `sphinxcontrib-jupyter` then you need to update
    `conf.py` file in your sphinx project.

Installation 
------------

To install `jupinx`:

.. code-block::

    pip install jupinx


to upgrade your current installation to the latest version:

.. code-block::
    
    pip install jupinx --upgrade

Usage
-----

To build a collection of notebooks using `jupinx`:

.. code-block::

    jupinx --notebooks <path_to_project>

.. note::

    Many users will run `jupinx` at the root level of a repository.
    this can be done by specifying :code:`jupinx --notebooks ./` 

It is also possible to build a full website. This option makes
use of Jupyter Notebooks ability to execute code so output is 
not required in any of the source files. The website can be 
completely built (including all code and generated components).

.. code-block::

    jupinx --website <path_to_project>

documentation regarding options for building websites can be found `here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-html.html>`__

You can also see all command line options available using:

.. code-block::
    
    jupinx --help


