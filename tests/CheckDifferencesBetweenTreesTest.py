# Path configuration for unit test 
import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from config import initLogger
from pathlib import Path
import unittest
from hashfileUtils import checkDifferencesBetweenTrees, printDifferencesBetweenTrees

class CheckDifferencesBetweenTreesTest(unittest.TestCase):

    def test_args_none(self) -> None:
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(None, dict())
        self.assertIsNotNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(dict(), None)
        self.assertIsNotNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None

    def test_empty_args(self) -> None:
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(dict(), dict())
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None
    
    def test_missing_folder(self) -> None:
        vFolder: Path = Path("virtualFolder\\")
        
        mapOfFileByFolder : dict[Path, set[Path]] = dict()
        fileInFolders : dict[Path, set[Path]] = dict()
        mapOfFileByFolder[vFolder] = set()
        
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 1)
        
        mapOfFileByFolder = dict()
        fileInFolders = dict()
        fileInFolders[vFolder] = set()

        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 1)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None
        
    def test_missing_file(self) -> None:
        vFolder: Path = Path("virtualFolder\\")
        vFile: Path = Path("virtualFolder\\file")
        
        mapOfFileByFolder : dict[Path, set[Path]] = dict()
        fileInFolders : dict[Path, set[Path]] = dict()
        mapOfFileByFolder[vFolder] = set([vFile])
        
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 1)
        
        mapOfFileByFolder = dict()
        fileInFolders = dict()
        fileInFolders[vFolder] = set([vFile])

        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 1)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None
    
    def test_common_folder(self) -> None:
        vFolder: Path = Path("virtualFolder\\")
        
        mapOfFileByFolder : dict[Path, set[Path]] = dict()
        fileInFolders : dict[Path, set[Path]] = dict()
        mapOfFileByFolder[vFolder] = set()
        fileInFolders[vFolder] = set()
        
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None

    def test_common_file(self) -> None:
        vFolder: Path = Path("virtualFolder\\")
        vFile: Path = Path("virtualFolder\\file")
        
        mapOfFileByFolder : dict[Path, set[Path]] = dict()
        fileInFolders : dict[Path, set[Path]] = dict()
        mapOfFileByFolder[vFolder] = set([vFile])
        fileInFolders[vFolder] = set([vFile])
        
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 0)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        return None
    
    def test_one_common_one_missing(self) -> None:
        vFolder: Path = Path("virtualFolder\\")
        v1File: Path = Path("virtualFolder\\file1")
        v2File: Path = Path("virtualFolder\\file2")
        
        mapOfFileByFolder : dict[Path, set[Path]] = dict()
        fileInFolders : dict[Path, set[Path]] = dict()
        mapOfFileByFolder[vFolder] = set([v1File, v2File])
        fileInFolders[vFolder] = set([v1File])
        
        missingInHashFileNotInDir : dict[Path, set[Path]]
        missingInDirNotInHashFile : dict[Path, set[Path]]
        error : Exception | None
        missingInHashFileNotInDir, missingInDirNotInHashFile, error = checkDifferencesBetweenTrees(mapOfFileByFolder, fileInFolders)
        self.assertIsNone(error)
        self.assertEqual(len(missingInHashFileNotInDir), 1)
        self.assertEqual(len(missingInDirNotInHashFile), 0)
        
        printDifferencesBetweenTrees(missingInHashFileNotInDir, missingInDirNotInHashFile)
        return None


if __name__ == '__main__':
    initLogger()
    unittest.main()

