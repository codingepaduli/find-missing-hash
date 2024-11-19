#!/bin/bash

# PYTHONDONTWRITEBYTECODE=1 -> don't create the folder __pycache__ running python3
# pyyaml --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

FOLDER_TO_CHECK="$HOME/SyncV2/AllDevices/Foto/"

FILE_TO_CHECK="$HOME/SyncV2/AllDevices/Foto/.checksum_2017-03-11-Foto_Sara.md5"

docker run -it --rm --name checkMissingItemsFromOneSource -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/checkMissingItemsFromOneSource.py --file $FILE_TO_CHECK "

