"""
    jupinx.cmd.quickstart
    ~~~~~~~~~~~~~~~~~~~~~

    Quickly setup documentation source to work with Jupinx.
"""

import argparse
import locale
import os
import subprocess
import sys
import pip

import time
import warnings
import importlib
from collections import OrderedDict
from os import path
from typing import Any, Callable, Dict, List, Pattern, Union
from distutils.dir_util import copy_tree

# try to import readline, unix specific enhancement
try:
    import readline
    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
        USE_LIBEDIT = True
    else:
        readline.parse_and_bind("tab: complete")
        USE_LIBEDIT = False
except ImportError:
    USE_LIBEDIT = False

from docutils.utils import column_width

import sphinx.locale
from jupinx import __display_version__, package_dir

from sphinx.deprecation import RemovedInSphinx40Warning
from sphinx.locale import __
from sphinx.util.console import (  # type: ignore
    colorize, bold, red, turquoise, nocolor, color_terminal
)
from sphinx.util.osutil import ensuredir
from jupinx.util.template import SphinxRenderer

TERM_ENCODING = getattr(sys.stdin, 'encoding', None)  # RemovedInSphinx40Warning

EXTENSIONS = OrderedDict([
    ('sphinxcontrib-jupyter', __('A Sphinx Extension for Generating Jupyter Notebooks')),
    ('sphinxcontrib-bibtex', __('A Sphinx extension for BibTeX style citations'))
])

PROMPT_PREFIX = '> '

if sys.platform == 'win32':
    # On Windows, show questions as bold because of color scheme of PowerShell (refs: #5294).
    COLOR_QUESTION = 'bold'
else:
    COLOR_QUESTION = 'purple'

KERNELLIST = OrderedDict([
    ('python3', {
        "kernelspec": {
            "display_name": "Python",
            "language": "python3",
            "name": "python3"
            },
        "file_extension": ".py",
    }),
    ('python2', {
        "kernelspec": {
            "display_name": "Python",
            "language": "python2",
            "name": "python2"
            },
        "file_extension": ".py",
    }),
    ('julia-1.1', {
        "kernelspec": {
            "display_name": "Julia 1.1",
            "language": "julia",
            "name": "julia-1.1"
            },
        "file_extension": ".jl"
    })
])

# function to get input from terminal -- overridden by the test suite
def term_input(prompt: str) -> str:
    if sys.platform == 'win32':
        # Important: On windows, readline is not enabled by default.  In these
        #            environment, escape sequences have been broken.  To avoid the
        #            problem, quickstart uses ``print()`` to show prompt.
        print(prompt, end='')
        return input('')
    else:
        return input(prompt)


class ValidationError(Exception):
    """Raised for validation errors."""


def is_path(x: str) -> str:
    x = path.expanduser(x)
    if not path.isdir(x):
        raise ValidationError(__("Please enter a valid path name."))
    return x


def allow_empty(x: str) -> str:
    return x


def nonempty(x: str) -> str:
    if not x:
        raise ValidationError(__("Please enter some text."))
    return x


def choice(*l: str) -> Callable[[str], str]:
    def val(x: str) -> str:
        if x not in l:
            raise ValidationError(__('Please enter one of %s.') % ', '.join(l))
        return x
    return val


def boolean(x: str) -> bool:
    if x.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError(__("Please enter either 'y' or 'n'."))
    return x.upper() in ('Y', 'YES')


def ok(x: str) -> str:
    return x


def term_decode(text: Union[bytes, str]) -> str:
    warnings.warn('term_decode() is deprecated.',
                  RemovedInSphinx40Warning, stacklevel=2)

    if isinstance(text, str):
        return text

    # Use the known encoding, if possible
    if TERM_ENCODING:
        return text.decode(TERM_ENCODING)

    # If ascii is safe, use it with no warning
    if text.decode('ascii', 'replace').encode('ascii', 'replace') == text:
        return text.decode('ascii')

    print(turquoise(__('* Note: non-ASCII characters entered '
                       'and terminal encoding unknown -- assuming '
                       'UTF-8 or Latin-1.')))
    try:
        return text.decode()
    except UnicodeDecodeError:
        return text.decode('latin1')


def do_prompt(text: str, default: str = None, validator: Callable[[str], Any] = nonempty) -> Union[str, bool]:  # NOQA
    while True:
        if default is not None:
            prompt = PROMPT_PREFIX + '%s [%s]: ' % (text, default)
        else:
            prompt = PROMPT_PREFIX + text + ': '
        if USE_LIBEDIT:
            # Note: libedit has a problem for combination of ``input()`` and escape
            # sequence (see #5335).  To avoid the problem, all prompts are not colored
            # on libedit.
            pass
        else:
            prompt = colorize(COLOR_QUESTION, prompt, input_mode=True)
        x = term_input(prompt).strip()
        if default and not x:
            x = default
        try:
            x = validator(x)
        except ValidationError as err:
            print(red('* ' + str(err)))
            continue
        break
    return x


class QuickstartRenderer(SphinxRenderer):
    def __init__(self) -> None:
        super().__init__()

    def render(self, template_name: str, context: Dict) -> str:
        user_template = path.basename(template_name)
        return super().render(template_name, context)


def ask_user(d: Dict) -> None:
    """Ask the user for quickstart values missing from *d*.

    Values are:

    * path:      root path
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    * language:  document language
    * kernels:   jupyter kernels
    * extensions:  extensions to use (list)
    """

    print(bold(__('Welcome to the Jupinx %s quickstart utility.')) % __display_version__)
    print()
    print(__('Please enter values for the following settings (just press Enter to\n'
             'accept a default value, if one is given in brackets).'))

    if 'path' in d:
        print()
        print(bold(__('Selected root path: %s')) % d['path'])
    else:
        print()
        print(__('Enter the root path for documentation.'))
        d['path'] = do_prompt(__('Root path for the documentation'), '.', is_path)

    while path.isfile(path.join(d['path'], 'conf.py')):
        print()
        print(bold(__('Error: an existing conf.py has been found in the '
                      'selected root path.')))
        print(__('jupinx-quickstart will not overwrite existing Jupinx projects.'))
        print()

        #### Will need to check if the below code is necessary
        # d['path'] = do_prompt(__('Press Enter to exit'),
        #                       '', is_path)
        if not d['path']:
            sys.exit(1)

    if 'project' not in d:
        print()
        print(__('The project name will occur in several places in the built documentation.'))
        d['project'] = do_prompt(__('Project name'))
    if 'author' not in d:
        d['author'] = do_prompt(__('Author name(s)'))

    if 'version' not in d:
        print()
        print(__('Jupinx has the notion of a "version" and a "release" for the\n'
                 'software. Each version can have multiple releases. For example, for\n'
                 'Python the version is something like 2.5 or 3.0, while the release is\n'
                 'something like 2.5.1 or 3.0a1.  If you don\'t need this dual structure,\n'
                 'just set both to the same value.'))
        d['version'] = do_prompt(__('Project version'), '', allow_empty)
    if 'release' not in d:
        d['release'] = do_prompt(__('Project release'), d['version'], allow_empty)

    if 'language' not in d:
        print()
        print(__('If the documents are to be written in a language other than English,\n'
                 'you can select a language here by its language code. Sphinx will then\n'
                 'translate text that it generates into that language.\n'
                 '\n'
                 'For a list of supported codes, see\n'
                 'https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.'))  # NOQA
        d['language'] = do_prompt(__('Project language'), 'en')
        if d['language'] == 'en':
            d['language'] = None

    #### DO WE NEED A DIFFERENT SUFFIX ?
    # if 'suffix' not in d:
    #     print()
    #     print(__('The file name suffix for source files. Commonly, this is either ".txt"\n'
    #              'or ".rst".  Only files with this suffix are considered documents.'))
    #     d['suffix'] = do_prompt(__('Source file suffix'), '.rst', suffix)

    #### DO WE NEED A DIFFERENT FILENAME THEN MASTER
    # if 'master' not in d:
    #     print()
    #     print(__('One document is special in that it is considered the top node of the\n'
    #              '"contents tree", that is, it is the root of the hierarchical structure\n'
    #              'of the documents. Normally, this is "index", but if your "index"\n'
    #              'document is a custom template, you can also set this to another filename.'))
    #     d['master'] = do_prompt(__('Name of your master document (without suffix)'), 'index')

    while path.isfile(path.join(d['path'], d['master'] + d['suffix'])) or \
            path.isfile(path.join(d['path'], 'source', d['master'] + d['suffix'])):
        print()
        print(bold(__('Error: the master file %s has already been found in the '
                      'selected root path.') % (d['master'] + d['suffix'])))
        print(__('jupinx-quickstart will not overwrite the existing file.'))
        print()
        d['master'] = do_prompt(__('Please enter a new file name, or rename the '
                                   'existing file and press Enter'), d['master'])

    ## Ask for kernels to include
    print()
    print(__('Select the kernels which you want for your jupyter notebook conversion'))
    for (key, value) in KERNELLIST.items():
        d['kernels'][key] = do_prompt('Do you want to have %s in your kernel list? (y/n)' % (key), 'y', boolean)

    # list of extensions to include in the conf file
    d['extensions'] = []

    # list of extensions which require installation
    d['toinstall'] = []

    ## Ask for sphinx extensions to be installed
    print(__('Indicate which of the following Sphinx extensions should be installed:'))
    for name, description in EXTENSIONS.items():
        moduleName = name.replace('-','.')
        try:
            importlib.import_module(moduleName)
            if do_prompt('%s package has been found in your system. Would you like to upgrade it? (y/n)' % (name), 'y', boolean):
                d['toinstall'].append(name)    
            d['extensions'].append(moduleName)
            
        except ImportError as e:
            if name == 'sphinxcontrib-jupyter':
                ## the extensions to install forcefully
                d['extensions'].append(moduleName)
                d['toinstall'].append(name)
            else:
                ## the extensions which are optional
                if do_prompt('%s: %s (y/n)' % (name, description), 'y', boolean):
                    d['extensions'].append(moduleName)
                    d['toinstall'].append(name)

    # # Handle conflicting options
    # if {'sphinx.ext.imgmath', 'sphinx.ext.mathjax'}.issubset(d['extensions']):
    #     print(__('Note: imgmath and mathjax cannot be enabled at the same time. '
    #                 'imgmath has been deselected.'))
    #     d['extensions'].remove('sphinx.ext.imgmath')
    print()


def generate(d: Dict, overwrite: bool = True, silent: bool = False
             ) -> None:
    """Generate project based on values in *d*."""
    template = QuickstartRenderer()
    if 'mastertoctree' not in d:
        d['mastertoctree'] = ''
    if 'mastertocmaxdepth' not in d:
        d['mastertocmaxdepth'] = 2

    d['now'] = time.asctime()
    d['project_underline'] = column_width(d['project']) * '='
    d['copyright'] = time.strftime('%Y') + ', ' + d['author']

    ensuredir(d['path'])

    basepath = d['path']

    srcdir = path.join(d['path'], 'source')

    ensuredir(srcdir)

    builddir = path.join(d['path'], '_build')
    d['exclude_patterns'] = ''
    ensuredir(builddir)
    
    themedir = path.join(d['path'], 'theme')
    ensuredir(themedir)
    ensuredir(path.join(themedir + '/templates'))
    ensuredir(path.join(srcdir + '/_static'))

    ## copying the html template files
    html_theme_path = os.path.join(package_dir, 'templates', 'html')
    copy_tree(html_theme_path + "/",themedir + '/templates/', preserve_symlinks=1)

    for (key, value) in KERNELLIST.items():
        if d['kernels'][key] is True:
            d['kernels'][key] = value

    def write_file(fpath: str, content: str, newline: str = None) -> None:
        if overwrite or not path.isfile(fpath):
            if 'quiet' not in d:
                print(__('Creating file %s.') % fpath)
            with open(fpath, 'wt', encoding='utf-8', newline=newline) as f:
                f.write(content)
        else:
            if 'quiet' not in d:
                print(__('File %s already exists, skipping.') % fpath)

    ## specifying the conf_path at present
    conf_path = os.path.join(package_dir, 'templates', 'quickstart', 'conf.py_t')
    with open(conf_path) as f:
        conf_text = f.read()

    write_file(path.join(basepath, 'conf.py'), template.render_string(conf_text, d))

    ## forming a minimal template of index.rst here
    masterfile = path.join(srcdir, d['master'] + d['suffix'])
    write_file(masterfile, template.render('quickstart/master_doc.rst_t', d))

    ## taking the minimal Makefile 
    makefile_template = 'quickstart/Makefile_t'

    d['rsrcdir'] = 'source'
    d['rbuilddir'] = '_build'
    # use binary mode, to avoid writing \r\n on Windows
    write_file(path.join(d['path'], 'Makefile'),
                template.render(makefile_template, d), '\n')

    ## install all the extensions specified in the extensions list
    for extension in d['toinstall']:
        install(extension)

    if silent:
        return
    print()
    print(bold(__('Finished: An initial directory structure has been created.')))
    print()
    print(__('You should now populate your master file %s and create other documentation\n'
             'source files. ') % masterfile, end='')
    print(__('Use the Makefile to build the docs, like so:\n'
                 '   make builder'))
    print(__('where "builder" is one of the supported builders, '
             'e.g. html, latex or linkcheck.'))
    print()


def valid_dir(d: Dict) -> bool:
    dir = d['path']
    if not path.exists(dir):
        return True
    if not path.isdir(dir):
        return False

    if {'Makefile', 'make.bat'} & set(os.listdir(dir)):
        return False

    reserved_names = [
        'conf.py',
        d['dot'] + 'static',
        d['dot'] + 'templates',
        d['master'] + d['suffix'],
    ]
    if set(reserved_names) & set(os.listdir(dir)):
        return False

    return True


# NEED TO ITERATE ON WHICH PARSER VARIABLES SHOULD BE NEEDED
def get_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Generate required files for a Jupinx project.\n"
        "\n"
        "jupinx-quickstart is an interactive tool that asks some questions about your\n"
        "project and then generates a complete documentation directory and sample\n"
        "Makefile to be used with jupinx-build.\n"
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        epilog=__("For more information, visit <https://github.com/QuantEcon/jupinx>."),
        description=description)
    return parser

## function to install packages via pip
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def main(argv: List[str] = sys.argv[1:]) -> int:
    sphinx.locale.setlocale(locale.LC_ALL, '')
    sphinx.locale.init_console(os.path.join(package_dir, 'locale'), 'sphinx')

    if not color_terminal():
        nocolor()

    ## parse options
    parser = get_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as err:
        return err.code

    d = vars(args)
    # delete None or False value
    d = {k: v for k, v in d.items() if v is not None}

    d.setdefault('extensions', [])
    # handle use of CSV-style extension values
    d.setdefault('toinstall', [])
    for ext in d['toinstall'][:]:
        if ',' in ext:
            d['toinstall'].remove(ext)
            d['toinstall'].extend(ext.split(','))

    ## Supporting .rst as the default suffix
    d.setdefault('suffix','.rst')
    d.setdefault('master','index')

    ## specifying kernels
    kernel_obj = {
        'python3': False,
        'python2': False,
        'julia-1.1': False
    }
    d.setdefault('kernels', kernel_obj)


    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print('[Interrupted.]')
        return 130  # 128 + SIGINT

    generate(d, overwrite=False)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
