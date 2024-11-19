from argparse import ArgumentParser
from pathlib import Path
import sys
from config import initLogger
import logging
from fileUtils import loadFileTree, searchHashFiles
from hashfileUtils import splitHashFileItemsByFolder, checkDifferencesBetweenTrees, printDifferencesBetweenTrees
from random import choice

if __name__ == "__main__":
    arg_parser = ArgumentParser(prog='findMissingItemInHashFile', allow_abbrev=False, description="find missing items between the file rows and the file listed in the file folder")
    arg_parser.add_argument(
            "-f",               # short parameter name
            "--file",         # long parameter name
            type=Path,          # argument type
            required=True,
            action="store",     # store the value in memory
            metavar='file',   # displayed name (in help messages)
            help="Option to select the folder where to search files."
        )
    arg_parser.add_argument(
            "-c",               # short parameter name
            "--check",           # long parameter name
            required=False,
            default='none',
            choices=['all', 'random'],
            nargs='?',          # only one item to choose
            action="store",     # store the value in memory
            help="Option to check all hash files or only a random file."
        )
    parsed_args = arg_parser.parse_args()
    
    initLogger()
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    missingHashFiles: set[Path]
    existentHashFiles: set[Path]
    error : Exception | None = None

    missingHashFiles, existentHashFiles, error = searchHashFiles(parsed_args.file)
    
    if error is not None:
        sys.exit(1)
    
    filenameInHashFileNotInDirSet : set[Path] = set()
    filenameInDirNotInHashFileSet : set[Path] = set()
    hashFilesToCheck : set[Path] = set()
    
    if parsed_args.check == 'random' and len(existentHashFiles)>0:
        randomFilename : Path = choice(list(existentHashFiles))
        logger.debug(f"choosing file: {randomFilename}")
        hashFilesToCheck.add(randomFilename)

    if parsed_args.check == 'all':
        logger.debug(f"choosing all files")
        hashFilesToCheck = existentHashFiles
    
    mapOfFileByFolder : dict[Path, set[Path]]
    
    hashFile : Path
    for hashFile in hashFilesToCheck:
        
        mapOfFileByFolder, error = splitHashFileItemsByFolder(hashFile)
        
        if error is not None:
            logger.error (f"error loading the file: {hashFile}: {error}")
            sys.exit(1)
        
        fileInFolders : dict[Path, set[Path]]
        fileInFolders, error = loadFileTree(hashFile.parent)
        
        if error is not None:
            logger.error (f" error iterating folder {hashFile.parent}: {error}")
            sys.exit(1)

        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        
        if error is not None:
            logger.error(f"Error checking the difference between trees: {error}")
            sys.exit(1)
        
        printDifferencesBetweenTrees(missingInHashFileNotInDir, missingInDirNotInHashFile)

