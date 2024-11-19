from config import initLogger
from pathlib import Path
from os import walk, strerror
import errno
import logging

def searchHashFiles(folder: Path) -> tuple[set[Path], set[Path], Exception | None]: 
    """
    Search recursively the hash files inside the folder 
    
    Starting from the folder path, recursively iterating in the directories and subdirectories, it will create a first set of folders with missing hash file inside and a second set of existent hash files 
    
    Parameters
    ----------
    folder: Path
        The folder where recursively search for hash files 

    Returns
    -------
    tuple[set[Path], set[Path], Exception | None]: 
        A first set of folders with missing hash file inside
        A second set of (existent) hash file
        Exception | None: 
            FileNotFoundError if the folder is None or is not a valid directory 
            OSError in case of error iterating folder and subfolders
            None in case of success (no error happens)
    """
    
    logger: logging.Logger = logging.getLogger(__name__)
    
    missingHashFiles: set[Path] = set()
    existentHashFiles: set[Path] = set()
    error: Exception | None = None
    
    if folder is None or not folder.is_dir():
        logger.error(f"folder doesn't exists:{folder}")
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), folder)
        return missingHashFiles, existentHashFiles, error
    
    root: str
    dirs: list[str]
    files: list[str]
    
    try:
        logger.debug(f"searching hash files in folder {folder}")
        for root, dirs, files in walk(folder):
            hashFiles: set[Path] = set (Path(root).glob("*.md5"))
            if len(hashFiles) == 0:
                missingHashFiles.add(Path(root))
            else:
                path: Path
                for path in hashFiles:
                    existentHashFiles.add(path)
        logger.debug(f"missing hash files {len(missingHashFiles)}, existent hash file {len(existentHashFiles)}")
    except OSError as ex:
        error = ex
        missingHashFiles = set()
        existentHashFiles = set()
        logger.exception(f"Error searching hash files in folder {folder}: {error}")

    return missingHashFiles, existentHashFiles, error


def loadFilesInDirectory(folder: Path) -> tuple[set[Path], Exception | None]:
    """
    Scan all the file in the directory 
    
    Parameters
    ----------
    folder: Path
        The folder to scan 

    Returns
    -------
    tuple[set[Path], Exception | None]
        A set of file in the folder 
        Exception | None: 
            FileNotFoundError if the folder is None or is not a valid folder 
            OSError in case of error iterating files
            None in case of success (no error happens)
    """
    
    logger: logging.Logger = logging.getLogger(__name__)

    fileList: set[Path] = set()
    error: Exception | None = None
    
    if folder is None or not folder.is_dir():
        logger.error(f"folder doesn't exists:{folder}")
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), folder)
        return fileList, error
    
    try:
        logger.debug(f"listing file in folder {folder}")
        child: Path
        for child in folder.iterdir():
            if child.is_file():
                fileList.add(child)
        logger.debug(f"files listed: {len(fileList)}")
    except OSError as ex:
        error = ex
        fileList = set()
        logger.exception(f"Error listing file in folder {folder}: {error}")
    
    return fileList, error

def loadFilesInDirectories(folders: set[Path]) -> tuple[dict[Path, set[Path]], Exception | None]:
    """
    Scan all the file in a set of existent folders 
    
    Parameters
    ----------
    folders: set[Path]
        The folders to scan 

    Returns
    -------
    tuple[dict[Path, set[Path]], Exception | None]
        A dict of folders, each folder bound to a set of file it contains 
        Exception | None: 
            ValueError if the folders parameter is None or is an empty set 
            OSError in case of error iterating folders, i.e. a folder doesn't exists
            None in case of success (no error happens)
    """
    
    logger: logging.Logger = logging.getLogger(__name__)
    
    fileInFolders: dict[Path, set[Path]] = dict()
    error: Exception | None = None
    
    if folders is None or len(folders) <= 0:
        logger.error(f"Expected a list of folders to load: {error}")
        error = ValueError("Expected a list of folders to load")
        return fileInFolders, error
    
    logger.debug(f"iterating {len(folders)} folders")
    
    fileCounter: int = 0
    folder: Path
    for folder in folders:
        filenameInDirectory: set[Path]
        filenameInDirectory, error = loadFilesInDirectory(folder)
        
        if error is not None:
            # remove all items from the dict and returns
            fileInFolders = dict()
            break
        
        # add the item into the dictionary
        fileCounter = fileCounter + len(filenameInDirectory)
        fileInFolders[folder] = filenameInDirectory
    
    logger.debug(f"Loaded {fileCounter} files from {len(folders)} folder")
    
    return fileInFolders, error


def splitFoldersByExistence(folders: set[Path]) -> tuple[set[Path], set[Path], Exception | None]:
    """
    Create a first set of existent folder and a second set of nonexistent or invalid folder 
    
    Parameters
    ----------
    folders: set[Path]
        The folders to split 

    Returns
    -------
    tuple[set[Path], set[Path], Exception | None]
        A dict of folders, each folder bound to a set of file it contains 
        Exception | None: 
            ValueError if the folders parameter is None or is an empty set 
            OSError in case of error iterating folders, i.e. a folder doesn't exists
            None in case of success (no error happens)
    """
        
    logger: logging.Logger = logging.getLogger(__name__)

    existentFolders : set[Path] = set()
    invalidFolders : set[Path] = set()
    error: Exception | None = None
    
    if folders is None or len(folders) <= 0:
        logger.error(f"Expected a list of folders to check: {error}")
        error = ValueError("Expected a list of folders to check")
        return existentFolders, invalidFolders, error
    
    logger.debug(f"splitting {len(folders)} folders by existence")

    folder: Path
    for folder in folders:
        if folder.is_dir():
            existentFolders.add(folder)
        else:
            invalidFolders.add(folder)
    
    logger.debug(f"valid folders {len(existentFolders)}, invalid folders {len(invalidFolders)}")
    
    return existentFolders, invalidFolders, error


def loadFileTree(rootFolder: Path) -> tuple[dict[Path, set[Path]], Exception | None]:
    """
    Scan all the file tree in a root folder 
    
    Parameters
    ----------
    folders: Path
        The root folder to scan 

    Returns
    -------
    tuple[dict[Path, set[Path]], Exception | None]
        A dict of folders, each folder bound to a set of file it contains 
        Exception | None: 
            ValueError if the folders parameter is None or is an empty set 
            OSError in case of error iterating folders, i.e. a folder doesn't exists
            None in case of success (no error happens)
    """
    logger: logging.Logger = logging.getLogger(__name__)
    
    fileTree : dict[Path, set[Path]] = dict()
    error: Exception | None = None
    
    if rootFolder is None or not rootFolder.is_dir():
        logger.error(f"folder doesn't exists:{rootFolder}")
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), rootFolder)
        return fileTree, error
    
    fileCounter: int = 0
    
    try:
        logger.debug(f"loading folder tree {rootFolder}")
        root: str
        dirs: list[str]
        files: list[str]
        for root, dirs, files in walk(rootFolder):
            fileFound : set[Path] = set (Path(root).glob("*.*"))
            fileTree[Path(root)] = fileFound
            fileCounter = fileCounter + len(fileFound)
        logger.debug(f"Loaded {fileCounter} files from folder tree {rootFolder}")
    except OSError as ex:
        error = ex
        fileTree = dict()
        logger.exception(f"Error loading folder tree {rootFolder}: {error}")

    return fileTree, error
