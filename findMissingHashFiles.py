from argparse import ArgumentParser
from pathlib import Path
import sys
from config import initLogger
import logging
from fileUtils import searchHashFiles

if __name__ == "__main__":
    """
    Print a lists of existent hash file and a list of folders without an hash file.
    
    Starting from the folder path, recursively iterating in the directories and subdirectories, it will create a first set of folders with missing hash file inside and a second set of existent hash files.
    
    The printed items depends from the command line options chosen:
    With the --show-missing option, it will print a list of folders with a missing hash file (*.md5, *.sha) inside.
    With the --show files option, it will print a list of existent hash file.
    Without --show-missing option and with --show none option, it will print nothing.
    """
    arg_parser = ArgumentParser(prog='findMissingHashFiles', allow_abbrev=False, description="find hash files in the current directory and each sub-directories")
    arg_parser.add_argument(
            "-f",               # short parameter name
            "--folder",         # long parameter name
            type=Path,          # argument type
            required=True,
            action="store",     # store the value in memory
            metavar='folder',   # displayed name (in help messages)
            help="Option to select the folder where to search files."
        )
    arg_parser.add_argument(
            "-m",               # short parameter name
            "--show-missing",   # long parameter name
            required=False,
            default=False,
            action="store_true",# store the value in memory
            help="Option to show the missing files."
        )
    arg_parser.add_argument(
            "-s",               # short parameter name
            "--show",           # long parameter name
            required=False,
            default='none',
            choices=['files', 'none'],
            nargs='?',          # only one item to choose
            action="store",     # store the value in memory
            help="Option to show the files, the folder or none of them."
        )
    parsed_args = arg_parser.parse_args()
    
    initLogger()
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    logger.info(f"searching file in folder {parsed_args.folder}")
    
    missingHashFiles: set[Path]
    existentHashFiles: set[Path]
    error : Exception | None
    missingHashFiles, existentHashFiles, error = searchHashFiles(parsed_args.folder)
    
    if error is not None:
        sys.exit(1)
    
    filename : Path
    if parsed_args.show_missing:
        logger.debug(f"found missing hash files: {len(missingHashFiles)}")
        for filename in missingHashFiles:
            print (f"{filename}")

    if parsed_args.show == 'files':
        logger.debug(f"found hash files: {len(existentHashFiles)}")
        for filename in existentHashFiles:
            print(f"{filename}")

