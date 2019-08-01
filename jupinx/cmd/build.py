"""
    jupinx.cmd.build
    ~~~~~~~~~~~~~~~~

    jupinx command-line handling.

"""

import argparse
import os
import subprocess
import sys
import copy
from typing import Dict, List

import locale
import sphinx.locale
from sphinx.locale import __
from jupinx import __display_version__, package_dir
import logging

ADDITIONAL_OPTIONS = [
    'directory',
    'parallel'
]

logging.basicConfig(format='%(levelname)s: %(message)s')
### This is a full blown manual and help tool which describes the functionality and usage of jupinx cmd
def get_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Jupinx command line tool.\n"
        "\n"
        "Provides a collection of utilities for Jupyter and Sphinx Projects.\n"
        "If you would like to setup a new project please use: jupinx-quickstart.\n"
        "\n"
    )
    epilog = __(
        "\n"
        "Examples:\n"
        "    jupinx --notebooks (within a project directory)\n"
        "    jupinx -n lecture-source-py (specify path to project directory)\n"
        "\n"
        "Further documentation is available: https://quantecon.github.io/jupinx/.\n"
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS] <DIRECTORY> [ADDITIONAL OPTIONS]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog,
        )
    parser.add_argument('directory', nargs='?', type=str, default='./', action='store', 
                        help="provide path to a project directory (optional)")
    parser.add_argument('-c', '--coverage', action='store_true', dest='coverage',
                        help="compile coverage report for project (result: _build/coverage/reports/{filename}.json")
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter',
                        help="compile a collection of Jupyter notebooks (result: _build/jupyter)")
    parser.add_argument('-w', '--website', action='store_true', dest='website',
                        help="compile a website through Jupyter notebooks (result: _build/website/")
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    group = parser.add_argument_group(__('additional options'))
    group.add_argument('--parallel', dest='parallel', nargs='?', type=int, const='2', action='store',
                        help='Specify the number of workers for parallel execution. [Default --parallel 2]')
    group.add_argument('-v', '--view', dest='view', nargs='?', type=str, const='notebooks', action='store',
                        help="Once build is complete open a server to view results. [Default --view='notebooks']")
    return parser

def check_directory_makefile(arg_dict):
    dir = None
    try:
        dir = arg_dict['directory']
    except:
        logging.error("Please specify a directory")
        return False

    if os.path.exists(dir) is False:
       logging.error("Specified directory does not exist")
       return False
    if os.path.isfile(dir + "/Makefile") is False:
       logging.error("Makefile not found in the directory")
       return False

def handle_make_parallel(cmd, arg_dict):
    if check_directory_makefile(arg_dict) is False:
        exit()
    if sys.version_info.major == 2:
        if 'parallel' in arg_dict:
            subprocess.call(['make', cmd, 'parallel=' + str(arg_dict['parallel'])], cwd=arg_dict['directory'])
        else:
            subprocess.call(['make', cmd], cwd=arg_dict['directory'])
    else:
        if 'parallel' in arg_dict:
            subprocess.run(['make', cmd, 'parallel=' + str(arg_dict['parallel'])], cwd=arg_dict['directory'])
        else:
            subprocess.run(['make', cmd], cwd=arg_dict['directory'])

def handle_make_preview(arg_dict):
    """
    Handle preview targeting from options specified through CLI
    TODO: Support individual lecture targeting
    """
    print(arg_dict['view'])
    target = str(arg_dict['view']).lower()
    if target == "website":
        cmd = ['make', 'preview', 'target=website']
        print("Running: " + " ".join(cmd))
        subprocess.run(cmd, cwd=arg_dict['directory'])
    elif target == "notebooks":
        cmd = ['make', 'preview']
        print("Running: " + " ".join(cmd))
        subprocess.run(cmd, cwd=arg_dict['directory'])
    else:
        logging.error("--view={} must be notebooks or website".format(target))

def make_file_actions(arg_dict: Dict):
    """
    Current Approach is to trigger calls to the Makefile contained in the project
    directory for sphinx-build using subprocesses.

    .. todo::

        Support sphinx-build directly using Invoke or some other library in the future
        will allow for advanced configuration options to be available through this tool.
    """
    if 'coverage' in arg_dict:
        handle_make_parallel('coverage', arg_dict)

    if 'website' in arg_dict:
        handle_make_parallel('website', arg_dict)

    if 'jupyter' in arg_dict:
        handle_make_parallel('jupyter', arg_dict)

    if 'view' in arg_dict:
        handle_make_preview(arg_dict)

def deleteDefaultValues(d):
    valid = False

    # delete None or False value and handle int and str for argparse const
    d = {k: v for k, v in d.items() if v is (not False) or (type(v) == int) or (type(v) == str) or isinstance(v, list)}
    temp = copy.deepcopy(d)

    # remove any additional options
    for option in ADDITIONAL_OPTIONS:
        if option in temp:
            del temp[option]

    if len(temp) > 0:
        valid = True

    return [d, valid]


def main(argv: List[str] = sys.argv[1:]) -> int:
    sphinx.locale.setlocale(locale.LC_ALL, '')
    sphinx.locale.init_console(os.path.join(package_dir, 'locale'), 'sphinx')

    ## parse options
    parser = get_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code
   
    d = vars(args)


    [d, valid] = deleteDefaultValues(d)

    ## no option specified then show help tool
    if valid is False:
        parser.print_help()
    else:
        make_file_actions(d)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))