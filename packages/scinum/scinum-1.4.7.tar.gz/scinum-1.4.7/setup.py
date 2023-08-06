# coding: utf-8


import os
from setuptools import setup

import scinum as sn


this_dir = os.path.dirname(os.path.abspath(__file__))


keywords = [
    "scientific", "numbers", "error", "systematics", "propagation",
]


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Information Technology",
]


# helper to read non-empty, stripped lines from an opened file
def readlines(f):
    for line in f.readlines():
        if line.strip():
            yield line.strip()


# read the readme file
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()


# load installation requirements
with open(os.path.join(this_dir, "requirements.txt"), "r") as f:
    install_requires = list(readlines(f))


# load docs requirements
with open(os.path.join(this_dir, "requirements_docs.txt"), "r") as f:
    docs_requires = [line for line in readlines(f) if line not in install_requires]


setup(
    name=sn.__name__,
    version=sn.__version__,
    author=sn.__author__,
    author_email=sn.__email__,
    description=sn.__doc__.strip().split("\n")[0].strip(),
    license=sn.__license__,
    url=sn.__contact__,
    keywords=keywords,
    classifiers=classifiers,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    extras_require={
        "docs": docs_requires,
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4",
    zip_safe=False,
    py_modules=[sn.__name__],
)
