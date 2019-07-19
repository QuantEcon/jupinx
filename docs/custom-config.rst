.. _custom_configuration:

Custom Configuration
====================

This project depends on `sphinxcontrib-jupyter <https://github.com/QuantEcon/sphinxcontrib-jupyter>`__
to modify `sphinx` to work with Jupyter notebooks. 

Full documentation for the extension can be found `here <http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest`__

An Example
----------

Let's say you have a collection of notebooks that you would like pre-executed. 
You can do this by modifying the ``conf.py`` file to enable notebook execution. 

Add the following in the ``conf.py`` in the `jupyter` options section:

.. code-block:: python

    jupyter_execute_notebooks = True

as documented `here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-execution.html#jupyter-execute-notebooks>`__

and let's imagine some of your documents produce a file required by a future 
document in your collection. An execution dependency can be added by:

.. code-block:: python

    jupyter_dependency_lists = {
        'lecture2' : ['lecture1']
        'lecture3' : ['lecture1']
        }

as documented `here <https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-extension-execution.html#jupyter-dependency-lists>`__