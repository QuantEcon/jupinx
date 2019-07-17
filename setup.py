# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = 'v0.0.1'

long_desc = '''
This package contains the Jupinx extension.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

install_requires = [
    'sphinxcontrib-jupyter',
    'docutils', 
    'nbformat', 
    'sphinx', 
    'dask', 
    'ipython', 
    'nbconvert', 
    'jupyter_client'
]

setup(
    name='Jupinx',
    version=VERSION,
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
            'jupinx-build = jupinx.cmd.build:main',
            'jupinx-quickstart = jupinx.cmd.quickstart:main'
        ]
    },
    install_requires=install_requires
)
