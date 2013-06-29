#!/usr/bin/env python

"""
avalon
-----

avalon -- Simulation framework

"""

from os import path as op

from setuptools import setup

from avalon import __version__, __project__, __license__


def read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''

install_requires = [l for l in read('requirements.txt').split('\n')
                    if l and not l.startswith('#')]


setup(
    name=__project__,
    version=__version__,
    license=__license__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=('Any'),
    keywords = "django sqlalchemy testing mongoengine stub mongoengine data".split(), # noqa

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url='http://github.com/klen/avalon',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    packages=['avalon'],
    install_requires=install_requires,
)

# lint_ignore=F0401
