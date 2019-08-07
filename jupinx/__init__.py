"""
    Jupinx
    ~~~~~~

    The Jupinx documentation toolchain.
"""

import os
import subprocess
import warnings
from os import path
from subprocess import PIPE

__version__ = '0.1.5'

package_dir = path.abspath(path.dirname(__file__))

__display_version__ = __version__  # used for command line version
