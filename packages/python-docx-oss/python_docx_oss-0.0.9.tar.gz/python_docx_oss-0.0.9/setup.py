#!/usr/bin/env python

import os
import pathlib
import re

from setuptools import find_packages, setup


def text_of(relpath):
    """
    Return string containing the contents of the file at *relpath* relative to
    this file.
    """
    thisdir = os.path.dirname(__file__)
    file_path = os.path.join(thisdir, os.path.normpath(relpath))
    return pathlib.Path(file_path).read_text()


# Read the version from docx.__version__ without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = re.search(r'__version__ = "([^"]+)"', text_of("docx/__init__.py"))[1]


NAME = "python-docx-oss"
VERSION = version
DESCRIPTION = "CRUD Microsoft Word .docx files."
KEYWORDS = "docx office openxml word python-docx-oss"
AUTHOR = "Ethan St. Lee"
AUTHOR_EMAIL = "ethan@ginolegaltech.cn"
URL = "https://github.com/lsaint/python-docx-oss"
LICENSE = text_of("LICENSE")
PACKAGES = find_packages(exclude=["tests", "tests.*"])
PACKAGE_DATA = {"docx": ["templates/*.xml", "templates/*.docx"]}

INSTALL_REQUIRES = ["lxml>=4.6.5"]
TEST_SUITE = "tests"
TESTS_REQUIRE = ["behave", "mock", "pyparsing", "pytest"]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Office/Business :: Office Suites",
    "Topic :: Software Development :: Libraries",
]

LONG_DESCRIPTION = text_of("README.md") + "\n\n" + text_of("HISTORY.md")

ZIP_SAFE = False

params = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "keywords": KEYWORDS,
    "long_description": LONG_DESCRIPTION,
    "long_description_content_type": "text/markdown",
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "url": URL,
    "license": LICENSE,
    "packages": PACKAGES,
    "package_data": PACKAGE_DATA,
    "install_requires": INSTALL_REQUIRES,
    "tests_require": TESTS_REQUIRE,
    "test_suite": TEST_SUITE,
    "classifiers": CLASSIFIERS,
    "zip_safe": ZIP_SAFE,
}

setup(**params)
