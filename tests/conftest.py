import os
import pytest

TEST_DIR = os.path.dirname(__file__)
CONTROL_DATA_1 = os.path.join(TEST_DIR, "control_data_1", "data_folder")
CONTROL_DATA_2 = os.path.join(TEST_DIR, "control_data_2", "data_folder")


@pytest.fixture
def txt_file_content():
    file_content = f"""COMPARISON OF FILES BETWEEN FOLDERS:
	FOLDER 1: {os.path.join(CONTROL_DATA_1)}
	FOLDER 2: {os.path.join(CONTROL_DATA_2)}


FILES ONLY IN: {os.path.join(CONTROL_DATA_1)}
	{os.path.join(CONTROL_DATA_1, "test_text.txt")}                |          0.00 bytes
	{os.path.join(CONTROL_DATA_1, "test_word.docx")}               |             5.03 KB
	{os.path.join(CONTROL_DATA_1, "test_folder", "test_image.bmp")}   |          0.00 bytes


FILES ONLY IN: {os.path.join(CONTROL_DATA_2)}
	None


FILES IN BOTH FOLDERS:
	{os.path.join(CONTROL_DATA_1, "test_excel.xlsx")}              |             6.35 KB
	{os.path.join(CONTROL_DATA_2, "test_excel.xlsx")}              |             6.35 KB
	{os.path.join(CONTROL_DATA_1, "test_powerpoint.pptx")}         |            32.27 KB
	{os.path.join(CONTROL_DATA_2, "test_powerpoint.pptx")}         |            32.27 KB
	{os.path.join(CONTROL_DATA_1, "test_zip.zip")}                 |             9.29 KB
	{os.path.join(CONTROL_DATA_2, "test_zip.zip")}                 |             9.41 KB
	{os.path.join(CONTROL_DATA_1, "test_folder", "test_folder_text.txt")}|          0.00 bytes
	{os.path.join(CONTROL_DATA_2, "test_folder", "test_folder_text.txt")}|          0.00 bytes

"""
    return file_content


@pytest.fixture
def csv_file_content():
    file_content = f'''"Files only in folder ""{os.path.join(CONTROL_DATA_1)}""",File size,"Files only in folder ""{os.path.join(CONTROL_DATA_2)}""",File size,"Files in both folders present on ""{os.path.join(CONTROL_DATA_1)}""",File size,"Files in both folders present on ""{os.path.join(CONTROL_DATA_2)}""",File size
{os.path.join(CONTROL_DATA_1, "test_text.txt")},0.00 bytes,,,{os.path.join(CONTROL_DATA_1, "test_excel.xlsx")},6.35 KB,{os.path.join(CONTROL_DATA_2, "test_excel.xlsx")},6.35 KB
{os.path.join(CONTROL_DATA_1, "test_word.docx")},5.03 KB,,,{os.path.join(CONTROL_DATA_1, "test_powerpoint.pptx")},32.27 KB,{os.path.join(CONTROL_DATA_2, "test_powerpoint.pptx")},32.27 KB
{os.path.join(CONTROL_DATA_1, "test_folder", "test_image.bmp")},0.00 bytes,,,{os.path.join(CONTROL_DATA_1, "test_zip.zip")},9.29 KB,{os.path.join(CONTROL_DATA_2, "test_zip.zip")},9.41 KB
,,,,{os.path.join(CONTROL_DATA_1, "test_folder", "test_folder_text.txt")},0.00 bytes,{os.path.join(CONTROL_DATA_2, "test_folder", "test_folder_text.txt")},0.00 bytes
'''
    return file_content
