#!/bin/bash

# PYTHONDONTWRITEBYTECODE=1 -> don't create the folder __pycache__ running python3
# pyyaml --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

FOLDER_TO_CHECK="$HOME/SyncV2/AllDevices/Foto/"

HASH_FILE="$HOME/SyncV2/AllDevices/Foto/2017-03-04_Weekend_Campi_Flegrei/cell/cell.md5"

docker run -it --rm --name checkMissingItemsInHashFile -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/checkMissingItemsInHashFile.py --file $HASH_FILE"

