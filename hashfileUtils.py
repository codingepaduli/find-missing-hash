from config import initLogger
from pathlib import Path
from os import strerror
import errno
import logging

def loadHashFile(filename: Path) -> tuple[dict[str, str], Exception | None]:
    """
    Load the hash file
   
    An hash file has each row filled with a relative file path, a double space separator and a hash of the file specified by the relative file path
    
    File:
      | filePath1  hash1 |
      | filePath2  hash2 |
      | filePath3  hash3 |
      | filePath4  hash4 |
      | filePath5  hash5 |
    
    This function loads all the rows in the file and store that in a dictionary of items, in which the item key is the relative file path and the item value is the hash
    
    dict: {
      filePath1->hash1
      filePath2->hash2
      filePath3->hash3
      filePath4->hash4
      filePath5->hash5
    }
    
    Parameters
    ----------
    filename : Path
        The hash file to load

    Returns
    -------
    tuple[dict[str, str], Exception | None]:
        A dictionary of items stored as filenames bound to their hashes
        Exception | None :
            FileNotFoundError if the filename is None or is not a valid file
            OSError in case of IO error loading the file
            None in case of success (no error happens)
    """
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    fileAndHashes : dict[str, str] = {}
    error : Exception | None = None

    if filename is None or not filename.is_file():
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), filename)
        logger.error(f"file doesn't exists: {filename}")
        return fileAndHashes, error
    
    lines : list[str] = []
    
    try:
        logger.debug(f"loading file {filename}")
        with open(filename) as f:
            lines = f.readlines()
    except OSError as ex:
        error = ex
        logger.exception(f"Error loading file {filename}: {error}")

    HASH : int = 0
    FILENAME : int = 1

    logger.debug(f"lines read: {len(lines)}")
    line : str
    for line in lines:
        lineParts :list[str] = line.replace("\r", "").replace("\n", "").split('  ')
        fileAndHashes[lineParts[FILENAME]] = lineParts[HASH]

    return fileAndHashes, error


def splitHashFileItemsByFolder(filename: Path) -> tuple[dict[Path, set[Path]], Exception | None]:
    """
    Split all the items inside the hash file by folder
    
    This function loads all the rows in the file and store that in a dictionary of items, in which the item key is the file path and the item value is a set of files listed in the hashfile
    
    dict: {
      folder1->{file1, file2, file3}
      folder2->{file4, file5, file6}
      folder3->{file7, file8}
      folder4->{file9}
      folder5->{}
    }
    
    Parameters
    ----------
    filename : Path
        The hash file to load

    Returns
    -------
    tuple[dict[Path, set[Path]], Exception | None]
        A dict of folder, each folder bound to the set of files it contains
        Exception | None :
            FileNotFoundError if the filename is None or is not a valid file
            OSError in case of error iterating folders
            None in case of success (no error happens)
    """
    
    mapOfFileByFolder: dict[Path, set[Path]] = dict()
    error : Exception | None = None
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    if filename is None or not filename.is_file():
        error = FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), filename)
        logger.error(f"filename doesn't exists: {error}")
        return mapOfFileByFolder, error

    fileAndHashes: dict[str, str]
    fileAndHashes, error = loadHashFile(filename)
    
    if error is not None:
        logger.exception(f"error loading hashfile:{error}")
        return mapOfFileByFolder, error
    
    rootFolder : Path = filename.parent
    
    if len(fileAndHashes) > 0:
        logger.debug (f"Filenames in hash file: {len(fileAndHashes)}")
        
        filepath : str
        hash: str
        for filepath, hash in fileAndHashes.items():
            fullPath : Path = rootFolder.joinpath(filepath)
            folder : Path = fullPath.parent
            
            # creating a map with a set of file, like the following:
            #   folder1 -> { filenameA, filenameB }
            #   folder3 -> { filename1, filename2, filename3 }
            
            # if the set of file exists, get the set
            # otherwise create a new set of files
            setOfFiles : set[Path]
            if folder in mapOfFileByFolder:
                setOfFiles = mapOfFileByFolder[folder]
            else:
                setOfFiles = set()
            
            # add the filename to the set
            setOfFiles.add(fullPath)
            
            # add the new set to the map
            mapOfFileByFolder[folder] = setOfFiles

    return mapOfFileByFolder, error


def checkDifferencesBetweenTrees(mapOfFileByFolder: dict[Path, set[Path]], fileInFolders: dict[Path, set[Path]]) -> tuple[dict[Path, set[Path]], dict[Path, set[Path]], Exception | None]:
    """
    Check the differences between the two trees
    
    The first tree contains all the file listed in the hash file, indexed by folder
    The second tree contains all the file listed in the root directory, indexed by folder
    
    This function returns a first dict of folders with files in the hash file and NOT in the root folder and a second dict of folders with files in the root folder and NOT in the hash file
    
    Parameters
    ----------
    mapOfFileByFolder: dict[Path, set[Path]]
        contains all the file listed in the hash file, indexed by folder
    fileInFolders: dict[Path, set[Path]]
        contains all the file listed in the root directory, indexed by folder

    Returns
    -------
    tuple[dict[Path, set[Path]], dict[Path, set[Path]], Exception | None]
        A first dict of folders with files in the hash file and NOT in the root folder
        A second dict of folders with files in the root folder and NOT in the hash file
        Exception | None : 
            ValueError if the param mapOfFileByFolder is None or the param fileInFolders is None
            None in case of success (no error happens)
    """
    logger : logging.Logger = logging.getLogger(__name__)
    
    missingInHashFileNotInDir : dict[Path, set[Path]] = dict()
    missingInDirNotInHashFile : dict[Path, set[Path]] = dict()
    error : Exception | None = None
    
    if mapOfFileByFolder is None:
        error = ValueError("map of folders from the hash file has an illegal value")
        logger.error(f"Expected to load a map of folders from the hash file: {error}.")
        return missingInHashFileNotInDir, missingInDirNotInHashFile, error
    
    if fileInFolders is None:
        error = ValueError("map of folders from a root folder has an illegal value")
        logger.error(f"Expected to load a map of folders from a root folder: {error}")
        return missingInHashFileNotInDir, missingInDirNotInHashFile, error

    # Common folders between the hash file and the root folder
    commonPaths : set[Path] = set(fileInFolders.keys()).intersection(set(mapOfFileByFolder.keys()))
    
    logger.debug(f"common folders between the root folder and the hash file: {len(commonPaths)}")

    folder: Path
    for folder in commonPaths:
        filesInHashFileSet : set[Path] = mapOfFileByFolder[folder]
        fileInFolderSet : set[Path] = fileInFolders[folder];
        
        filenameInHashFileNotInDirSet : set[Path] = filesInHashFileSet - fileInFolderSet
        filenameInDirNotInHashFileSet : set[Path] = fileInFolderSet - filesInHashFileSet

        logger.debug(f"Differences in common folder {folder}: {len(filenameInHashFileNotInDirSet)} items in hashfile - {len(filenameInDirNotInHashFileSet)} items in root folder")
        
        if len(filenameInHashFileNotInDirSet) > 0:
            missingInHashFileNotInDir[folder] = filenameInHashFileNotInDirSet
        
        if len(filenameInDirNotInHashFileSet) > 0:
            missingInDirNotInHashFile[folder] = filenameInDirNotInHashFileSet
    
    # folders missing only in the root directory, not in the hash file
    foldersOnlyInHashFile = set(mapOfFileByFolder.keys()) - set(fileInFolders.keys())
    logger.debug(f"not common folders missing only in the root directory, not in the hash file: {len(foldersOnlyInHashFile)}")
    
    for folder in foldersOnlyInHashFile:
        logger.debug(f"OnlyInHashFile: {folder}")
        missingInDirNotInHashFile[folder] = mapOfFileByFolder[folder]
    
    # folders missing only in the hash file, not in the root directory
    foldersOnlyInRootDir = set(fileInFolders.keys()) - set(mapOfFileByFolder.keys())
    logger.debug(f"not common folders missing only in the hash file, not in the root directory: {len(foldersOnlyInRootDir)}")
    
    for folder in foldersOnlyInRootDir:
        logger.debug(f"OnlyInRootDir: {folder}")
        missingInHashFileNotInDir[folder] = fileInFolders[folder]
    
    return missingInHashFileNotInDir, missingInDirNotInHashFile, error


def printDifferencesBetweenTrees(missingInHashFileNotInDir: dict[Path, set[Path]], missingInDirNotInHashFile: dict[Path, set[Path]]) -> None:
    """
    Print the two trees
    
    The first tree contains a map of folders, each folder is bound to a set of folder's file NOT existent in the hash file
    The second tree contains a map of folders, each folder is bound to a set of folder's file NOT existent in the root folder
    
    This function prints these files by folder. If a map is None, it will print nothing
    
    Parameters
    ----------
    mapOfFileByFolder: dict[Path, set[Path]]
        contains a map of folders, each folder is bound to a set of folder's file NOT existent in the hash file
    fileInFolders: dict[Path, set[Path]]
        contains a map of folders, each folder is bound to a set of folder's file NOT existent in the root folder
    """
    
    logger : logging.Logger = logging.getLogger(__name__)
    
    if missingInHashFileNotInDir is None:
        error = ValueError("map of folders from the hash file has an illegal value")
        logger.error(f"Expected to load a map of folders from the hash file: {error}")
        return None
    
    if missingInDirNotInHashFile is None:
        error = ValueError("map of folders from a root folder has an illegal value")
        logger.error(f"Expected to load a map of folders from the hash file: {error}")
        return None
    
    folder: Path
    missingFile: Path
    if len(missingInDirNotInHashFile) == 0:
        print ("All files in directory are in the hash file.")
    else:
        print ("Files in directory but NOT in hash file:")
        for folder in missingInDirNotInHashFile:
            print(folder)
            for missingFile in missingInDirNotInHashFile[folder]:
                print(f"\t {missingFile.name}")
    
    if len(missingInHashFileNotInDir) == 0:
        print ("All files in hash file are in the root directory.")
    else:
        print ("Files in hash file but NOT in the root directory:")
        for folder in missingInHashFileNotInDir:
            print(folder)
            for missingFile in missingInHashFileNotInDir[folder]:
                print(f"\t {missingFile.name}")
    
    return None