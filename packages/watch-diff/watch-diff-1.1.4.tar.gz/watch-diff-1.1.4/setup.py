"""
"""

import re
from setuptools import setup, find_packages


with open("watch_diff/__init__.py") as f:
    version = re.search(r"__version__ = \"(\d+\.\d+\.\d+)\"", f.read()).group(1)

with open("README.md") as f:
    long_description = f.read()

setup(
    name="watch-diff",
    version=version,
    description="Watch command output and get notified on changes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="francisbergin",
    author_email="francisbergin@hotmail.com",
    python_requires=">=3.7",
    url="https://github.com/francisbergin/watch-diff",
    packages=["watch_diff"],
    extras_require={
        "dev": [
            "black==23.1.0",
            "setuptools==67.4.0",
            "tox==4.4.6",
            "twine==4.0.2",
            "wheel==0.38.4",
        ]
    },
    license="MIT",
    entry_points={
        "console_scripts": [
            "watch-diff = watch_diff.__main__:main",
        ],
    },
)
