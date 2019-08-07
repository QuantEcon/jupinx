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
from notebook import notebookapp
from traitlets.config import Config

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
                            (Optional: the current working directory (./) is the default)
                            """.lstrip("\n"))
    )
    parser.add_argument('-c', '--clean', action='store_true', dest='clean',
                        help=textwrap.dedent("""
                        clean build directory
                        """.lstrip("\n"))
    )
    parser.add_argument('-j', '--jupyternb', action='store_true', dest='jupyternb',
                        help=textwrap.dedent("""
                        open jupyter to view notebooks
                        """.lstrip("\n"))
    )
    parser.add_argument('-n', '--notebooks', action='store_true', dest='jupyter',
                        help=textwrap.dedent("""
                            compile RST files to Jupyter notebooks
                             """.lstrip("\n"))
    )
    parser.add_argument('-s', '--server', action='store_true', dest='html-server',
                        help=textwrap.dedent("""
                        open html server to view website
                        """.lstrip("\n"))
    )
    parser.add_argument('-t', '--coverage-tests', action='store_true', dest='coverage',
                        help=textwrap.dedent("""
                            compile coverage report for project
                            """.lstrip("\n"))
    )
    parser.add_argument('-w', '--website', action='store_true', dest='website',
                        help=textwrap.dedent("""
                            compile website 
                            """.lstrip("\n"))
    )
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)
    group = parser.add_argument_group(__('additional options'))
    group.add_argument('-p', '--parallel', dest='parallel', nargs='?', type=int, const='2', action='store',
                        help=textwrap.dedent("""
                            Specify the number of workers for parallel execution 
                            (Default: --parallel will result in --parallel=2)
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

def handle_make_jupyternb(arg_dict):
    """ Launch Jupyter notebook server """
    if check_directory_makefile(arg_dict) is False:
        exit()
    if check_view_result_directory("notebooks", arg_dict) is False:
        exit()

    ## getting the build folder
    build_folder = arg_dict['directory'] + '_build/jupyter/'

    ## Note: we can support launching of individual files in the future ##

    cfg = Config()
    # cfg.NotebookApp.file_to_run = os.path.abspath(filename)
    cfg.NotebookApp.notebook_dir = build_folder
    cfg.NotebookApp.open_browser = True
    notebookapp.launch_new_instance(config=cfg,
                                    argv=[],  # Avoid it seeing our own argv
                                    )

def handle_make_htmlserver(arg_dict):
    """ Launch HTML Server (PORT = 8901) """
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading
    
    PORT = 8901
    webdir = arg_dict['directory'] + "_build/website/jupyter_html/"

    def start_server(httpd):
        httpd.serve_forever()

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=webdir, **kwargs)

    if check_directory_makefile(arg_dict) is False:
        exit()
    if check_view_result_directory("website", arg_dict) is False:
        exit()
    httpd = HTTPServer(("", PORT), Handler)
    print("Serving at http://localhost:{}".format(PORT))
    x = threading.Thread(target=start_server, args=(httpd,))
    x.start()
    webbrowser.open("http://localhost:{}".format(PORT))
    try:
        response = input("\nTo close the server please use Ctrl-C\n\n")
    except KeyboardInterrupt:
        print("Shutting down http server ...")
        httpd.shutdown()

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

    if 'jupyternb' in arg_dict:
        handle_make_jupyternb(arg_dict)
    
    if 'html-server' in arg_dict:
        handle_make_htmlserver(arg_dict)

def check_project_path(path):
    """ Check supplied project directory is valid and complete """
    path = os.path.normpath(path) + "/"
    if os.path.isdir(path):
        return path
    else:
        logging.error("The supplied project directory {} is not found".format(path))
        exit(1)

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
        d['directory'] = check_project_path(d['directory'])
        make_file_actions(d)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
