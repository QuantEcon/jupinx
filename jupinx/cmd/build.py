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
import webbrowser
import textwrap

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
        formatter_class=argparse.RawTextHelpFormatter,
        description=description,
        epilog=epilog,
        )
    parser.add_argument('directory', nargs='?', type=str, default='./', action='store', 
                        help=textwrap.dedent("""
                            provide path to a project directory
                            [Optional: './' will be assumed if not specified]
                            """.lstrip("\n"))
    )
    parser.add_argument('-c', '--clean', action='store_true', dest='clean',
                        help=textwrap.dedent("""
                        clean build so sphinx recompiles all source documents
                        """.lstrip("\n"))
    )
    parser.add_argument('-j', '--jupyterhub', action='store_true', dest='jupyterhub',
                        help=textwrap.dedent("""
                        open jupyter server when build completes to view notebooks
                        """.lstrip("\n"))
    )
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter',
                        help=textwrap.dedent("""
                            compile a collection of Jupyter notebooks
                            [Result: _build/jupyter]
                             """.lstrip("\n"))
    )
    parser.add_argument('-s', '--server', action='store_true', dest='html-server',
                        help=textwrap.dedent("""
                        open html server when build completes to view website
                        """.lstrip("\n"))
    )
    parser.add_argument('-t', '--coverage-tests', action='store_true', dest='coverage',
                        help=textwrap.dedent("""
                            compile coverage report for project
                            [Result: <project-directory>/_build/coverage/reports/{filename}.json]
                            """.lstrip("\n"))
    )
    parser.add_argument('-w', '--website', action='store_true', dest='website',
                        help=textwrap.dedent("""
                            compile a website through Jupyter notebooks
                            [Result: _build/website/]
                            """.lstrip("\n"))
    )
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    group = parser.add_argument_group(__('additional options'))
    group.add_argument('-p', '--parallel', dest='parallel', nargs='?', type=int, const='2', action='store',
                        help=textwrap.dedent("""
                            Specify the number of workers for parallel execution 
                            [Default: --parallel will result in --parallel=2 if no value is specified]
                            """.lstrip("\n"))
    )
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

def check_view_result_directory(target, arg_dict):
    if target == "notebooks":
        dir = arg_dict['directory'] + "_build/jupyter/"
    elif target == "website":
        dir = arg_dict['directory'] + "_build/website/jupyter_html/"
    else:
        logging.error("target must be directory or website for the -v, --view option")
    if os.path.exists(dir) is False:
        if target == "notebooks":
            logging.error("Results directory: {} does not exist!\nPlease run jupinx -n to build notebooks".format(dir))
        elif target == "website":
            logging.error("Results directory: {} does not exist.\n Please run jupinx -w to build website".format(dir))
        return False

def handle_make_parallel(cmd, arg_dict):
    if check_directory_makefile(arg_dict) is False:
        exit()
    if sys.version_info.major == 2:
        if 'parallel' in arg_dict:
            cmd = ['make', cmd, 'parallel=' + str(arg_dict['parallel'])]
            print("Running: " + " ".join(cmd))
            subprocess.call(cmd, cwd=arg_dict['directory'])
        else:
            cmd = ['make', cmd]
            print("Running: " + " ".join(cmd))
            subprocess.call(cmd, cwd=arg_dict['directory'])
    else:
        if 'parallel' in arg_dict:
            cmd = ['make', cmd, 'parallel=' + str(arg_dict['parallel'])]
            print("Running: " + " ".join(cmd))
            subprocess.run(cmd, cwd=arg_dict['directory'])
        else:
            cmd = ['make', cmd]
            print("Running: " + " ".join(cmd))
            subprocess.run(cmd, cwd=arg_dict['directory'])

def handle_make_jupyterhub(arg_dict):
    """ Launch Jupyterhub Server (PORT = 8900) """
    PORT = 8900
    if check_directory_makefile(arg_dict) is False:
        exit()
    if check_view_result_directory("notebooks", arg_dict) is False:
        exit()
    cmd = ['make', 'preview', 'PORT={}'.format(PORT)]
    print("Running: " + " ".join(cmd))
    catch_keyboard_interrupt("notebooks", cmd, arg_dict['directory'], PORT)

def handle_make_htmlserver(arg_dict):
    """ Launch HTML Sever (PORT = 8901) """
    PORT = 8901
    if check_directory_makefile(arg_dict) is False:
        exit()
    if check_view_result_directory("website", arg_dict) is False:
        exit()
    cmd = ['make', 'preview', 'target=website', 'PORT={}'.format(PORT)]
    print("Running: " + " ".join(cmd))
    catch_keyboard_interrupt("website", cmd, arg_dict['directory'], PORT)

def catch_keyboard_interrupt(target, cmd, cwd, port):
    """ Run subprocess.run call to catch Keyboard Interrupts """
    try:
        p = subprocess.Popen(cmd, cwd=cwd)
        # subprocess.run(cmd, cwd=cwd)
        if target == "website":
            webbrowser.open("http://localhost:{}".format(port))
        print("\nTo close the server press Ctrl-C\n")
        #Wait for User to use Ctrl-C
        while p:
            pass
    except KeyboardInterrupt:
        if target == 'notebooks':
            subprocess.run(['jupyter', 'notebook', 'stop', '{}'.format(port)])   #Stop Notebook Server
            p.kill()                                                  #Kill process
            print("\nClosing notebook server on port {}".format(port))
        else:
            print("\nClosing website server process on port {}".format(port))

def make_file_actions(arg_dict: Dict):
    """
    Current Approach is to trigger calls to the Makefile contained in the project
    directory for sphinx-build using subprocesses.

    .. todo::

        Support sphinx-build directly using Invoke or some other library in the future
        will allow for advanced configuration options to be available through this tool.
    """
    if 'clean' in arg_dict:
        if sys.version_info.major == 2:
            cmd = ['make', 'clean']
            print("Running: " + " ".join(cmd))
            subprocess.call(cmd, cwd=arg_dict['directory'])
        else:
            cmd = ['make', 'clean']
            print("Running: " + " ".join(cmd))
            subprocess.run(cmd, cwd=arg_dict['directory'])

    if 'coverage' in arg_dict:
        handle_make_parallel('coverage', arg_dict)

    if 'website' in arg_dict:
        handle_make_parallel('website', arg_dict)

    if 'jupyter' in arg_dict:
        handle_make_parallel('jupyter', arg_dict)

    if 'jupyterhub' in arg_dict:
        handle_make_jupyterhub(arg_dict)
    
    if 'html-server' in arg_dict:
        handle_make_htmlserver(arg_dict)


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