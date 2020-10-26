#!/bin/bash
# Simple PyPI publishing script

# Build the dist
python setup.py sdist bdist_wheel

# Upload using PyPI (test)
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload using PyPI (prod)
twine upload dist/*

# Cleanup
rm -rf build
rm -rf dist
rm -rf collapse.egg_info
