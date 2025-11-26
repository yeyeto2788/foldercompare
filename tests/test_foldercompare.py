"""Test the foldercompare.py module."""

import filecmp
import os
import shutil
import time
import unittest

import foldercompare


TEST_DIR = os.path.dirname(__file__)
FOLDER1 = os.path.join(TEST_DIR, "control_data_1", "data_folder")
FOLDER2 = os.path.join(TEST_DIR, "control_data_2", "data_folder")
RESULTS_FILE = os.path.join(TEST_DIR, "results")


class TestRecursiveDircmpReport(unittest.TestCase):
    """Test the _recursive_dircmp function."""

    def setUp(self):
        """Create two folders for testing."""
        self.folder1 = os.path.join("tests", "results1")
        self.folder2 = os.path.join("tests", "results2")
        os.makedirs(self.folder1, exist_ok=True)
        os.makedirs(self.folder2, exist_ok=True)

    @unittest.skip("Fails half the time -- enough to avoid same_files feature")
    def test_dircmp_diff_files_accuracy(self):
        """Different files are identified as such using filecmp.dircmp()"""

        file1 = os.path.join(self.folder1, "hello_world.txt")
        with open(file1, "w+") as file:
            file.write("foo")

        file2 = os.path.join(self.folder2, "hello_world.txt")
        with open(file2, "w+") as file:
            file.write("bar")

        comparison = filecmp.dircmp(self.folder1, self.folder2)
        time.sleep(0.2)
        self.assertTrue(comparison.diff_files == ["hello_world.txt"])
        self.assertTrue(comparison.same_files == [])

    def test_file_in_both(self):
        """Classifies two identical files as the same."""

        file1 = os.path.join(self.folder1, "hello_world.txt")
        with open(file1, "w+") as file:
            file.write("hello world")

        file2 = os.path.join(self.folder2, "hello_world.txt")
        with open(file2, "w+") as file:
            file.write("hello world")

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        self.assertIn("hello_world.txt", report["both"][0])

    def test_file_only_in_left(self):
        """Classifies file only in one directory."""

        file1 = os.path.join(self.folder1, "hello_world.txt")
        with open(file1, "w+") as file:
            file.write("hello world")

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        self.assertIn("hello_world.txt", report["left"][0])

    def test_subdirectory_only_in_left(self):
        """Classifies subdirectory with file only in left folder."""

        subdir1 = os.path.join(self.folder1, "subdir")
        os.makedirs(subdir1, exist_ok=True)

        file1 = os.path.join(subdir1, "hello_world.txt")
        with open(file1, "w+") as file:
            file.write("hello world")

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        self.assertIn("subdir", report["left"][0])

    def test_subdir_file_only_in_left(self):
        """Classifies file only in one subdirectory."""

        subdir1 = os.path.join(self.folder1, "subdir")
        subdir2 = os.path.join(self.folder2, "subdir")
        [os.makedirs(dir, exist_ok=True) for dir in [subdir1, subdir2]]

        file1 = os.path.join(subdir1, "hello_world.txt")
        with open(file1, "w+") as file:
            file.write("hello world")

        report = foldercompare._recursive_dircmp(self.folder1, self.folder2)
        self.assertIn(os.path.join("subdir", "hello_world.txt"), report["left"][0])

    def tearDown(self):
        """Delete test folders after each run."""
        shutil.rmtree(self.folder1)
        shutil.rmtree(self.folder2)


def test_create_txt(txt_file_content):
    """Can create a single TXT file, identical to the control."""

    foldercompare.compare(FOLDER1, FOLDER2, RESULTS_FILE, output_txt=True)

    with open(f"{RESULTS_FILE}.txt") as result:
        data = result.read()

    assert data.strip() == txt_file_content.strip()

    if os.path.exists(f"{RESULTS_FILE}.txt"):
        os.remove(f"{RESULTS_FILE}.txt")


def test_create_csv(csv_file_content):
    """Can create a single CSV file, identical to the control."""

    foldercompare.compare(FOLDER1, FOLDER2, RESULTS_FILE, output_csv=True)

    with open(f"{RESULTS_FILE}.csv") as result:
        data = result.read()

    assert data.strip() == csv_file_content.strip()

    if os.path.exists(f"{RESULTS_FILE}.csv"):
        os.remove(f"{RESULTS_FILE}.csv")


def test_create_both(csv_file_content, txt_file_content):
    """Can create both files at once, identical to the control."""

    foldercompare.compare(
        FOLDER1,
        FOLDER2,
        RESULTS_FILE,
        output_txt=True,
        output_csv=True,
    )

    with open(f"{RESULTS_FILE}.csv") as result:
        csv_data = result.read()

    with open(f"{RESULTS_FILE}.txt") as result:
        txt_data = result.read()

    assert txt_data.strip() == txt_file_content.strip()
    assert csv_data.strip() == csv_file_content.strip()

    for path in [f"{RESULTS_FILE}.csv", f"{RESULTS_FILE}.txt"]:
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
