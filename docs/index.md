---
title: /
layout: default
permalink: /
---

* * *


### Installation

To install `Jupinx`:

```
pip install jupinx
```

to upgrade your current installation to the latest version:

```
pip install jupinx --upgrade
```



## Get Started

The following is a very quick introduction to `jupinx`.  More details can be found in the [tutorial](tutorial.md).


### Source Repositories

The `jupinx` command line tool acts on a *source directory*, which must contain

* some RST files, including one called `index.rst` and

* a configuration file called `conf.py`.

(A `jupinx-quickstart` executable is available to help you setup a valid source directory.)


### Usage

Let's say you have a valid source directory called `source_directory` 

```
$ ls source_directory 

_build  conf.py  Makefile  source  theme
```

To convert the RST files in `source_directory` into notebooks, use

```
$ jupinx --notebooks source_directory
```

You can also use the short version:

```
$ jupinx -n source_directory
```

(Or, if you are at the root level of `source_directory`, you can just type `jupinx -n`.)

To view the results using Jupter Notebooks, type

```
$ jupinx -j source_directory
```

To convert the RST files into a website, use

```
$ jupinx -w source_directory
```

To view this website,  use

```
$ jupinx -s source_directory
```

To see more detail on these commands, type

```
$ jupinx --help
```

More details can be found in the [documentation](https://jupinx.readthedocs.io/).


### Advanced Configuration

In the tasks listed above, much of the heavy lifting is performed by 
the [sphinxcontrib-jupyter extension](https://github.com/QuantEcon/sphinxcontrib-jupyter).

See the documentation of that project for additional information.
