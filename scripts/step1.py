"""
Downloads the data in a zip file, reads its contents and generates a
new csv file with the fields we need.
"""

import csv
from zipfile import ZipFile

import requests


def download():
    """Downloads the dataset and saves it to disk."""

    url = "https://www.ssa.gov/oact/babynames/names.zip"

    with requests.get(url) as response:

        with open("names.zip", "wb") as temp_file:
            temp_file.write(response.content)


def parse_zip():
    """Reads the contents of the zip file and creates a csv file with them."""

    # This list will hold all our data. We initialize it with the header row.
    data_list = [["year", "name", "gender", "count"]]

    # We first read the zip file using a zipfile.ZipFile object.
    with ZipFile("names.zip") as temp_zip:

        # Then we read the file list.
        for file_name in temp_zip.namelist():

            # We will only process .txt files.
            if ".txt" in file_name:

                # Now we read the current file from the zip file.
                with temp_zip.open(file_name) as temp_file:

                    # The file is opened as binary, we decode it using utf-8 so it can be manipulated as a string.
                    for line in temp_file.read().decode("utf-8").splitlines():

                        # We prepare our desired data fields and add them to the data list.
                        line_chunks = line.split(",")
                        year = file_name[3:7]
                        name = line_chunks[0]
                        gender = line_chunks[1]
                        count = line_chunks[2]

                        data_list.append([year, name, gender, count])

    # We save the data list into a csv file.
    csv.writer(open("data.csv", "w", newline="",
                    encoding="utf-8")).writerows(data_list)


if __name__ == "__main__":

    download()
    parse_zip()
