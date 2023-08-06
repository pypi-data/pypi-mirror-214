#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for pyrestyle."""
import io
from setuptools import setup

# read the contents of your README file

INSTALL_REQUIRES = (
    ['tabulate >= 0.9.0', 'tomli; python_version < "3.11"']
)

def get_version():
    with open('pyrestyle.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

with io.open('README.rst') as readme:
    setup(
        name='pyrestyle',
        version=get_version(),
        description="Python style guide checker and This project based on pycodestyle",
        long_description=readme.read(),
        keywords='pyrestyle, pep8, PEP 8, PEP-8, PEP8',
        author='Johann C. Rocholl, 2023-1-OPPS1-CGS-08',
        author_email='kys00919@gmail.com',
        url='https://github.com/CSID-DGU/2023-1-OPPS1-CGS-08/blob/main/pyrestyle.py',
        license='Expat license',
        py_modules=['pyrestyle'],
        include_package_data=True,
        zip_safe=False,
        python_requires='>=3.7',
        entry_points={
            'console_scripts': [
                'pyrestyle = pyrestyle:_main',
            ],
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )