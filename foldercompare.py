"""Compare the content of two folders and create report(s) of result."""

import csv
import filecmp
import os
import zipfile
import shutil


def compare(folder1, folder2, output, output_txt=False, output_csv=False):
    """
    Compare contents of two folders and write a report of the results.

    Args:
        folder1: String with the directory of left folder.
        folder2: String with the directory of right folder.
        output: Description of parameter `output`.
        output_txt: Boolean variable to create an '.txt' file.
        output_csv: Boolean variable to create an '.csv' file.

    Returns:
        Nothing.
    """

    bln_remove_dir = [False, False]

    if zipfile.is_zipfile(folder1) or folder1.endswith(".zip"):
        with zipfile.ZipFile(folder1, "r") as myzip:
            unzipped1 = os.path.join(
                os.path.abspath(os.path.join(folder1, os.pardir)), "folder1"
            )
            myzip.extractall(unzipped1)
            folder1 = unzipped1
            bln_remove_dir[0] = True

    if zipfile.is_zipfile(folder2) or folder2.endswith(".zip"):
        with zipfile.ZipFile(folder2, "r") as myzip:
            unzipped2 = os.path.join(
                os.path.abspath(os.path.join(folder2, os.pardir)), "folder2"
            )
            myzip.extractall(unzipped2)
            folder2 = unzipped2
            bln_remove_dir[1] = True

    # Make filepath names for output OS-agnostic
    folder1 = os.path.normpath(folder1)
    folder2 = os.path.normpath(folder2)

    report = _recursive_dircmp(folder1, folder2, folder1, folder2)

    if output_txt:
        _write_to_plain_text(folder1, folder2, output, report)

    if output_csv:
        _write_to_csv(folder1, folder2, output, report)

    if bln_remove_dir[0]:
        shutil.rmtree(unzipped1, ignore_errors=True)

    if bln_remove_dir[1]:
        shutil.rmtree(unzipped2, ignore_errors=True)


def _convert_bytes(num):
    """
    This function will convert bytes to KB, MB.

    Args:
        num: Integer with the number of bytes.

    Returns:
        String with values converted.
    """

    for x in ["bytes", "KB", "MB"]:
        if num < 1024.0:
            return "%3.2f %s" % (num, x)
        num /= 1024.0


def _file_size(file_path):
    """
    This function will return the file size if file exists on the filesystem.

    Args:
        file_path: String with the file path to chak its size.

    Returns:
        strReturn: String of the file's size converted.
    """

    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        strReturn = _convert_bytes(file_info.st_size)
    else:
        strReturn = ""

    return strReturn


def _recursive_dircmp(folder1, folder2, prefix1=".", prefix2="."):
    """
    Return a recursive dircmp comparison report as a dictionary.

    Args:
        folder1: String with the directory of left folder.
        folder2: String with the directory of right folder.
        prefix1: String with the prefix of the directory 1 being searched.
        prefix2: String with the prefix of the directory 2 being searched.

    Returns:
        data: Dictionary with the file comparison.
    """

    comparison = filecmp.dircmp(folder1, folder2)

    data = {
        "left": ["{}{}{}".format(prefix1, os.sep, i) for i in comparison.left_only],
        "right": ["{}{}{}".format(prefix2, os.sep, i) for i in comparison.right_only],
        "both": [
            "{}{}{}***{}{}{}".format(prefix1, os.sep, i, prefix2, os.sep, i)
            for i in comparison.common_files
        ],
    }

    for datalist in data.values():
        datalist.sort()

    if comparison.common_dirs:
        for folder in comparison.common_dirs:
            # Update prefix to include new sub_folder
            prefix1 = os.path.normpath(os.path.join(folder1, folder))
            prefix2 = os.path.normpath(os.path.join(folder2, folder))
            # Compare common folder and add results to the report
            sub_folder1 = os.path.join(folder1, folder)
            sub_folder2 = os.path.join(folder2, folder)
            sub_report = _recursive_dircmp(sub_folder1, sub_folder2, prefix1, prefix2)

            # Add results from sub_report to main report
            for key, value in sub_report.items():
                data[key] += value

    return data


def _write_to_plain_text(folder1, folder2, output, report):
    """
    Write the comparison report to a plain text file.

    Args:
        folder1: String with the directory of left folder.
        folder2: String with the directory of right folder.
        output: String with the directory to write the '.txt' file.
        report: Dictionary with the data to be written on the file.

    Returns:
        Nothing.
    """

    filename = output + ".txt"
    with open(filename, "w") as file:
        file.write("COMPARISON OF FILES BETWEEN FOLDERS:\n")
        file.write("\tFOLDER 1: {}\t\t{}\n".format(folder1, _file_size(folder1)))
        file.write("\tFOLDER 2: {}\t\t{}\n".format(folder2, _file_size(folder2)))
        file.write("\n\n")

        file.write("FILES ONLY IN: {}\n".format(folder1))
        for item in report["left"]:
            if item is not None:
                file.write(
                    f"\t{item:<100}|{str(_file_size(os.path.join(folder1, item))):>20}\n"
                )
        if not report["left"]:
            file.write("\tNone\n")
        file.write("\n\n")

        file.write("FILES ONLY IN: {}\n".format(folder2))
        for item in report["right"]:
            if item is not None:
                file.write(
                    f"\t{item:<100}|{str(_file_size(os.path.join(folder2, item))):>20}\n"
                )
        if not report["right"]:
            file.write("\tNone\n")
        file.write("\n\n")

        file.write("FILES IN BOTH FOLDERS:\n")
        for item in report["both"]:
            item1, item2 = item.split("***")
            file.write(
                f"\t{item1:<100}|{str(_file_size(os.path.join(folder1, item1))):>20}\n"
            )
            file.write(
                f"\t{item2:<100}|{str(_file_size(os.path.join(folder2, item2))):>20}\n"
            )
        if not report["both"]:
            file.write("\tNone\n")


def _write_to_csv(folder1, folder2, output, report):
    """
    Write the comparison report to a CSV file for use in Excel.

    Args:
        folder1: String with the directory of left folder.
        folder2: String with the directory of right folder.
        output: String with the directory to write the '.csv' file.
        report: Dictionary with the data to be written on the file.

    Returns:
        Nothing.
    """

    filename = output + ".csv"
    with open(filename, "w") as file:
        csv_writer = csv.writer(file, dialect="excel", lineterminator="\r")

        # Write header data to the first row
        headers = (
            'Files only in folder "{}"'.format(folder1),
            "File size",
            'Files only in folder "{}"'.format(folder2),
            "File size",
            'Files in both folders present on "{}"'.format(folder1),
            "File size",
            'Files in both folders present on "{}"'.format(folder2),
            "File size",
        )
        csv_writer.writerow(headers)

        # Order report data to match with headers
        data = (
            report["left"],
            [_file_size(x) for x in report["left"]],
            report["right"],
            [_file_size(x) for x in report["right"]],
            [x.split("***")[0] for x in report["both"]],
            [_file_size(x.split("***")[0]) for x in report["both"]],
            [x.split("***")[1] for x in report["both"]],
            [_file_size(x.split("***")[1]) for x in report["both"]],
        )

        # Write comparison data row by row to the CSV
        row_index = 0
        row_max = max(len(column) for column in data)
        while row_index < row_max:
            values = []
            for column in data:
                # Use data from column if it exists, otherwise use None
                try:
                    values += [column[row_index]]
                except IndexError:
                    values += [None]

            csv_writer.writerow(values)
            row_index += 1
