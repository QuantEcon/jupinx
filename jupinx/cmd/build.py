"""
    jupinx.cmd.build
    ~~~~~~~~~~~~~~~~

    jupinx command-line handling.

"""

import argparse
import locale
import os
import re
import subprocess
import sys
import pip

import time
import warnings
import importlib
from collections import OrderedDict
from os import path
import subprocess
from typing import Dict, List

import sphinx.locale
from sphinx.locale import __
from jupinx import __display_version__, package_dir
from sphinx.util.osutil import ensuredir

### This is a full blown manual and help tool which describes the functionality and usage of jupinx cmd
def get_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Jupinx command line tool.\n"
        "\n"
        "Provides a collection of utilities for Jupyter and Sphinx Projects.\n"
        "If you would like to setup a new project please use: jupinx-quickstart.\n"
        "\n"
        "Examples:\n"
        "    jupinx --notebooks (within a project directory)\n"
        "    jupinx -n -d lecture-source-py (specified path to project directory)\n"
        "\n"
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog="Further documentation is available: https://quantecon.github.io/jupinx/.\n",
        )
    parser.add_argument('-c', '--coverage', action='store_true', dest='coverage',
                        help="compile coverage report for project (result: _build/coverage/reports/{filename}.json")
    parser.add_argument('-d', '--directory', action='store_true', dest="directory", 
                        help="provide path to a project directory")
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter',
                        help="compile a collection of Jupyter notebooks (result: _build/jupyter)")
    parser.add_argument('-w', '--website', action='store_true', dest='website',
                        help="compile a website through Jupyter notebooks (result: _build/website/")
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    return parser

### This is a minimum help tool which can be shown in cases where the user has not input any options to jupinx cmd
def get_minimum_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Jupinx command line tool.\n"
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description=description)
    parser.add_argument('-d', '--directory', action='store_true', dest='directory')
    parser.add_argument('-c', '--coverage', action='store_true', dest='coverage')
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter')
    parser.add_argument('-w', '--website', action='store_true', dest='website')
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    return parser

def make_file_actions(arg_dict: Dict):
    """
    Current Approach is to trigger calls to the Makefile contained in the project
    directory for sphinx-build using subprocesses.

    .. todo::

        Support sphinx-build directly using Invoke or some other library in the future
        will allow for advanced configuration options to be available through this tool.
    """
    if 'website' in arg_dict:
        if sys.version_info.major == 2:
            subprocess.call(['make','website'])
        else:
            subprocess.run(['make','website'])
    elif 'coverage' in arg_dict:
        if sys.version_info.major == 2:
            subprocess.call(['make','coverage'])
        else:
            subprocess.run(['make','coverage'])
    elif 'jupyter' in arg_dict:
        if sys.version_info.major == 2:
            subprocess.call(['make','jupyter'])
        else:
            subprocess.run(['make','jupyter'])


def main(argv: List[str] = sys.argv[1:]) -> int:
    sphinx.locale.setlocale(locale.LC_ALL, '')
    sphinx.locale.init_console(os.path.join(package_dir, 'locale'), 'sphinx')

    ## parse options
    parser = get_parser()
    minimal_parser = get_minimum_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code
   
    d = vars(args)
    # delete None or False value
    d = {k: v for k, v in d.items() if v is not False}
    
    ## no option specified then show a minimal help tool
    if not d:
        minimal_parser.print_help()
    else:
        make_file_actions(d)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))