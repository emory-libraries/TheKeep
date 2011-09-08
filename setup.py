#!/usr/bin/env python

from setuptools import setup, find_packages
import keep

LONG_DESCRIPTION = None
try:
    # read the description if it's there
    with open('README.rst') as desc_f:
        LONG_DESCRIPTION = desc_f.read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='keep',
    version=keep.__version__,
    author='Emory University Libraries',
    author_email='libsysdev-l@listserv.cc.emory.edu',
    url='https://svn.library.emory.edu/digital_masters',
    license='Apache License, Version 2.0',
    packages=find_packages(),

    install_requires=[
        'eulxml',
        'rdflib>=3.0',
        'python-dateutil',
        'soaplib==0.8.1',
    ],

    # indexdata utils are optional. They include things like PDF text stripping (pyPdf).
    # Be sure to include the below in your own pip dependencies file if you need to use
    # the built in indexer utility support.
    extras_require = {
        'indexdata_util': ['pyPdf',],
    },

    description='Bare bones install of the keep to allow for use of its models.',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
)
