#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    author="Andrew Moss",
    author_email="andrew.moss@neofinancial.com",
    python_requires=">=3.6",
    name="erdgen",
    version="0.1.1",
    description="Generate a DBML ERD from DBT YML relationships",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    license="MIT license",
    packages=find_packages(include=["erdgen", "erdgen.*"]),
    url="https://github.com/neo-andrew-moss/erdgen",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["click", "PyYAML", "Jinja2", "typing_extensions"],
    tests_require=["pytest"],
)
