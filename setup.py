"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

from __future__ import print_function
from setuptools import setup,find_packages
from codecs import open
from os import path
from setuptools.dist import Distribution
import sys

proj_dir = path.abspath(path.dirname(__file__))

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def has_ext_modules(self):
        return True


with open(path.join(proj_dir,'README.md'), encoding='utf-8') as fid:
    long_description = fid.read()

setup(
    name='dssvue',

    version = '0.1',

    description ='GUI for HEC-DSS database file',

    long_description = long_description,

    url = '',

    author = 'Gyan Basyal',

    author_email = 'gyanBasyalz@gmail.com',


    license = 'MIT',

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Water resources engineers :: Developers',
        'Operating System :: Windows',
        'Programming Language :: Python :: 3',
     ],

    packages = find_packages(),


    package_data = {'':['*.txt','*.md',
                        'LICENSE',
                        'ui/*',
                        '*.py',
                        'examples/*']},

    include_package_data = True,

    data_files=[],

    distclass = BinaryDistribution,

    install_requires = ['numpy', 'pandas', 'affine','pyqt5','pyqtgraph'],

    python_requires='>=3.6, <3.8',

    zip_safe = False,

    )
