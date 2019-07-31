.. _sphinxcontrib-jupyter:

Custom Configuration through `sphinxcontrib-jupyter <https://github.com/QuantEcon/sphinxcontrib-jupyter>`__
===========================================================================================================

This project depends on `sphinxcontrib-jupyter <https://github.com/QuantEcon/sphinxcontrib-jupyter>`__
to enhance ``sphinx`` to build and work with Jupyter notebooks. 

Full documentation for the extension can be found `here <http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest>`__

There are many configuration settings that can adjust the compilation behaviour of your project.

An Example
----------

Let's say you have a collection of notebooks that you would like pre-executed. 
You can do this by modifying the ``conf.py`` file to enable notebook execution. 

Add the following in the ``conf.py`` in the `jupyter` options section:

.. code-block:: python

    jupyter_execute_notebooks = True

as documented `here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-execution.html#jupyter-execute-notebooks>`__

and let's imagine some of your documents produce a file required by a future 
document in your collection. An execution dependency can be added to your project by 
specifying:

.. code-block:: python

    jupyter_dependency_lists = {
        'lecture2' : ['lecture1']
        'lecture3' : ['lecture1']
        }

in the ``conf.py`` file as documented `here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-execution.html#jupyter-dependency-lists>`__