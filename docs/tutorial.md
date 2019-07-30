---
title: Tutorial
layout: default
permalink: /tutorial.html
---

Tutorial: Setting up a Project
==============================

This tutorial will take you through the steps needed to get up and running. 

Step 1: Installing Package
--------------------------

Make sure you have `jupinx` installed. It can be installed using `pip`:

```bash
pip install jupinx
```

Step 2: Create a Sphinx Project
-------------------------------

Navigate to your working directory and create a folder for your project

```bash
mkdir jupinx-project
```

You can then use the `jupinx-quickstart` utility to setup the project quickly with 
some basic configuration already in place:

```bash
cd jupinx-project
jupinx-quickstart
```

The `quickstart-utility` will take you through a series of questions to assist with 
this configuration:

```bash
Welcome to the Jupinx 0.0.1 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Enter the root path for documentation.
> Root path for the documentation [.]: 

The project name will occur in several places in the built documentation.
> Project name: First Jupinx Project
> Author name(s): QuantEcon

Jupinx has the notion of a "version" and a "release" for the
software. Each version can have multiple releases. For example, for
Python the version is something like 2.5 or 3.0, while the release is
something like 2.5.1 or 3.0a1.  If you don\'t need this dual structure,
just set both to the same value.
> Project version []: 0.1
> Project release [0.1]: 

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]: 

Select the kernels which you want for your jupyter notebook conversion
> Do you want to have python3 in your kernel list? (y/n) [y]: 
> Do you want to have python2 in your kernel list? (y/n) [y]: n
> Do you want to have julia-1.1 in your kernel list? (y/n) [y]: n
Indicate which of the following Sphinx extensions should be installed:
> sphinxcontrib-jupyter package has been found in your system. Would you like to upgrade it? (y/n) [y]: n
> sphinxcontrib-bibtex package has been found in your system. Would you like to upgrade it? (y/n) [y]: n

Creating file ./conf.py.
Creating file ./source/index.rst.
Creating file ./Makefile.

Finished: An initial directory structure has been created.

You should now populate your master file ./source/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

and you should now see the following files and folders in your directory:

```bash
Makefile	_build		conf.py		source		theme
```

This is the structure adopted by the `jupinx` project. You can now start building Jupyter 
notebooks using `jupinx`

```bash
jupinx --notebooks
```

As there is not content in this project we should first create our first source file.

Step 3: Writing your first RST Source File
------------------------------------------

The `source` directory is the place that should contain all your source `rst` files. 

Let's create a file `first_notebook.rst` in the `source` directory and add the following:

```rst
First Notebook
==============

This is our first notebook and it will contain the following code-block.

.. code-block:: python

    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        title='About as simple as it gets, folks')
    ax.grid()

```

You will need to also add `first_notebook` to the `toctree` in your `source/index.rst` file.

Step 4: Building your Project
-----------------------------

Now in your project folder `jupinx-project` you can start building your project:

```bash
jupinx --notebooks
```

will generate notebooks from the `rst` files and place them in `_build/jupyter/`

You can open a jupyter server in this directory to see the results

```bash
cd _build/jupyter
jupyter notebook
```

.. note:: 

    In future this should be added to `jupinx`. See [Issue #21](https://github.com/QuantEcon/jupinx/issues/21)


Step 5: Advanced Configuration of `sphinxcontrib-jupyter`
---------------------------------------------------------

Now that we have succesfully built your first notebook we can set that notebook to execute 
by enabling the execution option in the `conf.py` file. 

You can open `conf.py` file and at the bottom of this file you can find sphinxcontrib-jupyter
options. You can add:

```python
jupyter_execute_notebooks = True
```

this will now build notebooks and then excecute them for you with results stored in 
`_build/jupyter/executed`. You can test this by:

```bash
make clean    #Clear Sphinx Cache to Rebuild Files from Scratch
make jupyter
```

.. note:: 

    The [sphinxcontrib-jupyter documentation](https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-project.html) has a section on Managing Large Projects that may require
    different compilation pipelines for editing and publishing. 
