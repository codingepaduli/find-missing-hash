from argparse import ArgumentParser
from pathlib import Path
import sys
from config import initLogger
import logging
from fileUtils import loadFileTree
from hashfileUtils import splitHashFileItemsByFolder, checkDifferencesBetweenTrees, printDifferencesBetweenTrees

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
    parsed_args = arg_parser.parse_args()
    
    initLogger()
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    mapOfFileByFolder : dict[Path, set[Path]]
    error : Exception | None
    mapOfFileByFolder, error = splitHashFileItemsByFolder(parsed_args.file)
    
    if error is not None:
        logger.error (f" error iterating folder {parsed_args.file} {error}")
        sys.exit(1)

    if len(mapOfFileByFolder) <= 0:
        logger.error(f"Empty file {parsed_args.file}")
        sys.exit(1)
    
    fileInFolders : dict[Path, set[Path]]
    fileInFolders, error = loadFileTree(parsed_args.file.parent)
    
    if error is not None:
        logger.error (f" error iterating folder {parsed_args.file.parent}: {error}")
        sys.exit(1)

    if len(fileInFolders) <= 0:
        logger.error(f"No files found in folder {parsed_args.file.parent}")
        sys.exit(1)
    
    missingInHashFileNotInDir : dict[Path, set[Path]]
    missingInDirNotInHashFile : dict[Path, set[Path]]
    missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
    
    if error is not None:
        logger.error(f"Error checking the difference between trees: {error}")
        sys.exit(1)
    
    printDifferencesBetweenTrees(missingInHashFileNotInDir, missingInDirNotInHashFile)
        