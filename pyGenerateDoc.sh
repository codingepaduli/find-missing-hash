#!/bin/bash


echo "Generating documentation TODO script to complete (impossible to use Sphinx from command line)" 

# using pydoc
#
# docker run -it --rm --name pydoc -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -w /usr/src/myapp python:3.10 /bin/bash -c 'pydoc -w /usr/src/myapp/findMissingHashFiles.py'

# Using Sphinx
# sphinx-quickstart generate a conf.py (configured from CLI) and a index.rst (from a template, uncustomizable from CLI)
#
# docker run -it --rm --name sphinx-doc -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -w /usr/src/myapp python:3.10 /bin/bash -c 'pip install -U Sphinx && sphinx-quickstart --no-sep --project=findMissingHashFiles --author=Me --release=0.1 -v 0.1 --language=en --ext-autodoc && sphinx-build -b html . docs'

# Using Sphinx
# sphinx-build starts the documentation generation, -C option avoids to read the conf.py file, -D sets the options of conf.py from command lines, -b option set to generate docs as html pages 
#
# docker run -it --rm --name sphinx-doc -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -w /usr/src/myapp python:3.10 /bin/bash -c 'pip install -U Sphinx && sphinx-build -C -D project=findMissingHashFiles -D author=Me -D release=0.1 -D version=0.1 -D language=en -b html . docs'

