---
title: /
layout: default
permalink: /
---

* * *

## Get Started

### Installation

To install `Jupinx`:

```
pip install jupinx
```

to upgrade your current installation to the latest version:

```
pip install jupinx --upgrade
```


### Quickstart

When starting your own projects a `jupinx-quickstart` is available that will guide you through the initial setup
of a sphinx project that is setup to use the [sphinxcontrib-jupyter](https://github.com/QuantEcon/sphinxcontrib-jupyter)
extension.

Open a terminal and make a folder for your project. Then run:

```
jupinx-quickstart
```

and follow the on-screen questions.

### Usage

To build a collection of notebooks using `Jupinx`:

```
jupinx --notebooks --directory <PATH>
```

You can also use short versions such as:

```
jupinx -n -d <PATH>
```

If you are at the root level of your project directory you can trigger a build 
without specifying the directory location:

```
jupinx --notebooks
```

You can also see the options available using:

```
jupinx --help
```

Additional compilation options are available and details can be found in the [documentation](https://jupinx.readthedocs.io/)


### Advanced Configuration

The `jupinx-quickstart` will get you up and running to build Jupyter notebooks. 
However you may want more advanced control of your project. 
The [sphinxcontrib-jupyter extension](https://github.com/QuantEcon/sphinxcontrib-jupyter) 
can be configured to:

1. Enable Notebook Execution (after construction)
1. Enable the construction of a website (from the ipynb collection)

Documentation can be found [here](https://jupinx.readthedocs.io/en/latest/?badge=latest)

