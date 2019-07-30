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
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS]',
        description=description)
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter')
    parser.add_argument('-c', '--coverage', action='store_true', dest='coverage')
    parser.add_argument('-w', '--website', action='store_true', dest='website')
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    
    group = parser.add_argument_group(__('additional options'))
    group.add_argument('--parallel', dest='parallel', nargs='?', type=int, const='2', action='store')
    return parser

### This is a minimum help tool which can be shown in cases where the user has not input any options to jupinx cmd
def get_minimum_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Minimal help tool.\n"
        "\n"
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS] ',
        description=description)
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter')
    parser.add_argument('-c', '--coverage', action='store_true', dest='coverage')
    parser.add_argument('-w', '--website', action='store_true', dest='website')
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)

    group = parser.add_argument_group(__('additional options'))
    group.add_argument('--parallel', dest='parallel', nargs='?', type=int, const='2', action='store')
    return parser

def handle_make_parallel(cmd, arg_dict):
    if sys.version_info.major == 2:
        if 'parallel' in arg_dict:
            subprocess.call(['make', cmd, 'parallel=' + str(arg_dict['parallel'])])
        else:
            subprocess.call(['make', cmd])
    else:
        if 'parallel' in arg_dict:
            subprocess.run(['make', cmd, 'parallel=' + str(arg_dict['parallel'])])
        else:
            subprocess.run(['make', cmd])

def make_file_actions(arg_dict: Dict):
    if 'coverage' in arg_dict:
        handle_make_parallel('coverage', arg_dict)

    if 'website' in arg_dict:
        handle_make_parallel('website', arg_dict)

    if 'jupyter' in arg_dict:
        handle_make_parallel('jupyter', arg_dict)


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

    # delete None or False value and handle int
    d = {k: v for k, v in d.items() if v is (not False and not None) or (type(v) == int)}

    ## no option specified then show a minimal help tool
    if not d:
        minimal_parser.print_help()
    else:
        make_file_actions(d)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))