# -*- coding: utf-8 -*-

import jupinx

from setuptools import setup, find_packages

VERSION = 'v0.1.2'

long_desc = '''
This package contains the Jupinx extension.

.. add description here ..
'''

install_requires = [
    'docutils', 
    'nbformat', 
    'sphinx>=1.8.5', 
    'dask', 
    'dask[distributed]',
    'ipython', 
    'nbconvert', 
    'jupyter_client',
    'pyzmq>=17.1.3'
]

setup(
    name='Jupinx',
    version=jupinx.__version__,
    url='https://github.com/QuantEcon/jupinx',
    download_url='https://github.com/QuantEcon/jupinx/archive/{}.tar.gz'.format(VERSION),
    license='BSD',
    author='QuantEcon',
    author_email='admin@quantecon.org',
    description='Jupinx extension: Convert your RST files into into different formats like notebook, pdf, html.',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'jupinx-quickstart = jupinx.cmd.quickstart:main',
            'jupinx = jupinx.cmd.build:main'
        ]
    },
    install_requires=install_requires
)
