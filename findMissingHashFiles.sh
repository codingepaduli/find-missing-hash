#!/bin/bash

# PYTHONDONTWRITEBYTECODE=1 -> don't create the folder __pycache__ running python3
# pyyaml --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

# BUG: bash pipe '|' and bash evaluation '$()' don't work with docker when 
# execute 'docker run -it'. Fix the bug using 'docker run -i'
# echo piped content | docker run -i  ubuntu:16.04 cat - # works
# echo piped content | docker run -it ubuntu:16.04 cat - # error: unable to setup input stream

FOLDER_TO_CHECK="$HOME/SyncV2/AllDevices/Foto/"

echo "missing hash files: "

docker run -it --rm --name findMissingHashFiles -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/findMissingHashFiles.py --folder $FOLDER_TO_CHECK --show-missing --show none"

echo "existent hash files: "

docker run -it --rm --name findMissingHashFiles -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/findMissingHashFiles.py --folder $FOLDER_TO_CHECK --show files"

#############################################################################
#                                   Script                                  #
#############################################################################

echo "choosing an hash file:"

hashFiles=$(docker run -i --rm --name findMissingHashFiles -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/findMissingHashFiles.py --folder $FOLDER_TO_CHECK --show files")

IFS=$'\n'  # split rows on \n into the for each loop
i=0
for item in $hashFiles
do
    #echo "$i $item"
    hashes+=($item)
    i=$((i+1))
done

size=${#hashes[@]}

randomIndex=$((RANDOM % size))

echo "choosing by random index: $randomIndex -> ${hashes[randomIndex]} <-"

