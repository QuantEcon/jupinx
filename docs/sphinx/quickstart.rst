.. _quickstart:

jupinx-quickstart
=================

A quickstart utility has been developed to help users get setup quickly 
with Sphinx, configured in a way to get building collections of Jupyter notebooks 
quickly. 

Installation
------------

To install `jupinx <https://github.com/QuantEcon/jupinx>`__:

.. warning::

    This project is **not** yet released through PyPI. Please instead install 
    using :code:`python setup.py install` from within a clone of the 
    repository.

.. code-block:: bash

    pip install jupinx

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
#. a parent document ``source/index.rst``

after running the quickstart you may run ``make jupyter`` to build the project

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

    ``sphinx`` is actually quite flexible in setting up a project in a way 
    that suits your workflow. If you want to change directory structure this 
    is likely possible but you will need to update your ``Makefile`` after the 
    quickstart is finished. Please refer to `sphinx docs <http://sphinx-doc.org>`__
    for further information.