.. _quickstart:

jupinx-quickstart
=================

A quickstart utility has been developed to help users get setup quickly 
with Sphinx, configured in a way to get building collections of Jupyter notebooks 
quickly. 

.. contents::
   :depth: 1
   :local:

Installation
------------

To install `jupinx <https://github.com/QuantEcon/jupinx>`__:

.. code-block:: bash

    pip install jupinx

or you can upgrade to the latest version using:

.. code-block:: bash

    pip install --upgrade jupinx

.. note::

    ``Windows`` is currently not tested or supported. 
    See `Issue #7 <https://github.com/QuantEcon/jupinx/issues/7>`_

Running :code:`jupinx-quickstart`
---------------------------------

Once, ``jupinx`` is installed, to run the jupinx quickstart program you can run:

.. code-block:: bash

    jupinx-quickstart

on a terminal. 

The ``jupinx-quickstart`` will:

#. setup a `directory structure <Directory_structure>`_ for your project
#. check for ``sphinxcontrib-jupyter`` and ``sphinxcontrib-bibtex`` installation
#. construct ``Makefile`` and ``conf.py`` files 
#. construct a parent document ``source/index.rst``
#. setup the project to use the ``minimal`` theme

after running the quickstart you may run:

#. ``make jupyter`` to build the project as notebooks
#. ``make website`` to build the project as a website (via sphinxcontrib-jupyter)
#. ``make pdf`` to build the project as a pdf (via sphinxcontrib-jupyter)

.. note::

    The ``quickstart`` sets up the `Makefile` with some `conf.py` setting overrides to
    enable building `jupyter` and `website` (rather than via a specific builder)

Directory structure
-------------------

The following directory structure is adopted during the setup:

- ``./``
    - ``source``: where source RST files should be added
    - ``source/_static``: where _static assets such as figures and images are kept
    - ``theme``: allows you to customise builders using themes and templates
    - ``Makefile``: provides ``make`` commands for compiling the project
    - ``conf.py``: provides configuration for ``sphinx-build``

.. note::

    ``sphinx`` is quite flexible in setting up a project in a way 
    that suits your workflow. If you want to change directory structure this 
    is likely possible but you will need to update your ``Makefile`` after the 
    quickstart is finished. Please refer to `sphinx docs <http://sphinx-doc.org>`__
    for further information.