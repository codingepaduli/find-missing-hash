#!/bin/bash

echo "Executing tests..."

# PYTHONDONTWRITEBYTECODE=1 -> don't create the folder __pycache__ running python3
# pyyaml --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

docker run -it --rm --name unittest -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c 'pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/tests/CheckDifferencesBetweenTreesTest.py'

