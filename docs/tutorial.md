---
title: Tutorial
layout: default
permalink: /tutorial.html
---

# Tutorial: Setting up a Project

This tutorial will take you through the steps needed to get up and running
with `jupinx`. 

For a guide on how to use `jupinx` on a Windows system, see [this page](/windows.html).

## Installation

Make sure you have `jupinx` installed: 

```bash
pip install --upgrade jupinx
```


## Understanding Source Directories

The `jupinx` command line tool converts RST files in a **source directory**
into 

1. a set of Jupyter Notebooks
2. a website, and/or
3. pdf files

A valid source directory must contain

* some RST files, including one called `index.rst` and

* a configuration file called `conf.py`

* a jupinx compatible `Makefile`


## Creating a Source Directory

One way to set up a valid source directory is via the `jupinx-quickstart` executable.

To use it, first create a folder for your project

```bash
mkdir jupinx-project
```

Now type

```bash
cd jupinx-project
jupinx-quickstart
```

(You can also specify a target folder as long as that folder already exists.) 

The `quickstart-utility` will take you through a series of questions:

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
where "builder" is one of the supported builders, e.g. jupyter, website or pdf.
```

You should now see the following files and folders in your directory:

```bash
ls jupinx-project

> Makefile	_build		conf.py		source		theme
```

.. note::

    ``jupinx-quickstart`` includes a `minimal` theme to enable html and pdf
    construction.

Now let's create our first source file.


## Writing an RST Source File

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


## Building and Viewing

Let's have a look at our project.

With `jupinx-project` in the present working directory, type

```bash
jupinx --notebooks jupinx-project
```

Alternatively, you can use the full path:

```bash
jupinx --notebooks /home/full/path/jupinx-project
```

You can also shorten to 

```bash
jupinx -n jupinx-project
```

(Or, if you are at the root level of `jupinx-project`, you can just type `jupinx -n`.) 

This generates notebooks from the `rst` files and puts them in `_build/jupyter/`

To view the results using Jupyter Notebooks, type

```
jupinx -j jupinx-project
```

To convert the RST files into a website, use

```
jupinx -w jupinx-project
```

To view this website,  use

```
jupinx -s jupinx-project
```

To see more detail on these commands, type

```
jupinx --help
```

More details can be found in the [documentation](https://jupinx.readthedocs.io/).


## Advanced Configuration 

Much of the heavy lifting for `jupinx` is done by a Sphinx extension called
[sphinxcontrib-jupyter](https://github.com/QuantEcon/sphinxcontrib-jupyter/)

For details on advanced configuration, see the [sphinxcontrib-jupyter documentation](https://sphinxcontrib-jupyter.readthedocs.io/en/latest/config-project.html).

As one example, we can set generated notebooks to execute by enabling the execution option in the `conf.py` file. 

Open `conf.py` file and at the bottom of this file you will find sphinxcontrib-jupyter options. You can add:

```python
jupyter_execute_notebooks = True
```

This will now build notebooks and then execute them for you with results stored in `_build/jupyter/executed`. You can test this by:

```bash
jupinx --clean --notebooks
```


