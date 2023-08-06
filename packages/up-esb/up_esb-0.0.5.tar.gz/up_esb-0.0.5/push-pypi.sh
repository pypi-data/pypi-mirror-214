#!/bin/bash -e

# How to release a new package version:
# 1. Change the version number in the pyproject.toml file
# 2. Run this script and login with your pypi account to upload

# install required packages if necessary
if ! pip3 show build > /dev/null 2>&1; then
    pip3 install build
fi

if ! pip3 show twine > /dev/null 2>&1; then
    pip3 install twine
fi

# delete old distribution
rm -rf dist *.egg-info

# build sdist and wheel
python3 -m build

# upload to pypi
python3 -m twine upload dist/*
