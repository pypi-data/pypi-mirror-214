import os
import re
from setuptools import setup

_long_description = open('README.md').read()

setup(
    name = "ganok",
    version = "1.1.0",
    author = "ganok mb",
    author_email = "testhost5023@gmail.com",
    description = (" library Rubika"),
    license = "MIT",
    keywords = ["ganok","Ganok"],
    url = "https://github.com",
    packages=['ganok'],
    long_description=_long_description,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
)