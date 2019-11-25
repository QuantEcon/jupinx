---
title: Windows
layout: default
permalink: /windows.html
---

# Tutorial: Using Jupinx with Windows

This tutorial will take you through some recommended steps to get `jupinx` running on a Windows system.

## Introduction

Jupinx is not natively supported in Windows, but it is possible to run Jupinx on a Linux subsystem using WSL (Windows Subsystem for Linux). Jupinx can be installed normally on the Linux subsystem, but will require some extra steps to work properly with Windows. 

Note: Windows 10 is required to use WSL.

## Step 1: Set up Ubuntu on WSL
We suggest you follow a tutorial like [this one by Microsoft](https://docs.microsoft.com/en-us/windows/wsl/install-win10). You can choose which Linux distro to use - we recommend Ubuntu simply because it was used in making this guide and we know it works. The rest of this guide assumes you are using Ubuntu.

## Step 2: Install Anaconda on Ubuntu
1. Open a web browser in Windows and navigate to Anaconda's download/distribution page [here](https://www.anaconda.com/distribution/). Your (Windows) operating system will be detected and you will be recommended the Windows installer. Don't download this one - you want the Linux version.
2. Right click on the Linux download link for Python 3 and and click Copy Link or Copy Link Location.
3. Open a Linux terminal (if using Ubuntu, simply search for Ubuntu in the Windows search bar). To download the Anaconda install files, type:

```bash
wget <Anaconda download link>
```

for example:

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
```

4. To install, run the installation script for whichever version of Anaconda you've got downloaded: 

```bash
bash Anaconda3<version>.sh
```

for example:

```bash
bash Anaconda3-2019.10-Linux-x86_64.sh
```

## Step 3: Install Jupinx on the Ubuntu subsystem
Open an Ubuntu terminal and follow the instructions [here](/tutorial.html) for installing Jupinx.

Check that the install has worked with: 

```bash
jupinx --version
```
Jupinx should now be working on Ubuntu, but you may encounter errors if editing .rst source files in Windows. Step 4 should resolve this problem.
### Viewing Jupyter notebooks
Jupyter notebooks usually launch in a browser, but will not find Windows browsers from the Ubuntu subsystem. Try typing 

```bash
jupyter notebook
```

If  everything is working properly, you should be provided with a URL you can enter in a Windows web browser to view the notebooks in your current directory, if there are any. 

## Step 4: Use Visual Studio Code extension 'Remote-WSL' to edit source .rst files

To avoid potential problems caused by differences in Windows and Linux file systems, we recommend you edit Jupinx source files in the Ubuntu system. One way to do this is with the VSCode 'Remote-WSL' extension.

1. Install VSCode
2. Install the Remote-WSL extension
3. To open a file called filename.rst in the VSCode Remote-WSL editor from Ubuntu, type the following in an Ubuntu terminal:

```bash
code filename.rst
```
You can also open an Ubuntu-side VSCode window through the menus.

>## Note
>
>A good rule of thumb is that wherever possible you should do things in Ubuntu, not Windows, to avoid compatibility problems. **If working with git, for instance, use it through the Ubuntu terminal** (not with a separate Windows installation of git).

## See Also
* [These instructions](https://github.com/QuantEcon/lecture-source-jl#usage) for editing the QuantEcon lectures using Jupinx on a Windows system
