"""
Downloads the data in a zip file, reads its contents and generates a
new csv file with the fields we need.
"""

import csv
import datetime
import requests

from io import BytesIO
from zipfile import ZipFile


def prettytime():
    """ returns formatted time string """
    return datetime.date.strftime(datetime.datetime.now(),
                                  "%Y%m%d T %H%M%S")


if __name__ == "__main__":

    ## Step 1: download the dataset and turn it into an in-memory zipfile

    url = "https://www.ssa.gov/oact/babynames/names.zip"

    print("[{nowish}] starting".format(nowish=prettytime()))
    with requests.get(url) as response:
        print("[{nowish}] response downloaded".format(nowish=prettytime()))
        temp_zip = ZipFile(BytesIO(response.content))
        print("[{nowish}] in-memory zip created".format(nowish=prettytime()))

    ## Step 2: Read the contents of the zip file and write out data as CSV

    # This list will hold all our data. We initialize it with the header row.
    data_list = [["year", "name", "gender", "count"]]

    # Construct the file list. We're only interested in the text
    # files; the PDF isn't useful for this purpose.
    allfiles = [f for f in temp_zip.namelist() if f.endswith(".txt")]

    for fn in allfiles:
        year = fn[3:7]
        if int(year) % 10 == 0:
            print("[{nowish}] processing year {year}".format(
                nowish=prettytime(), year=year))

        # Extract this year's file to memory
        with temp_zip.open(fn) as temp_file:

            # The file is opened as binary, we decode it using
            # utf-8 so it can be manipulated as a string.
            for line in temp_file.read().decode("utf-8").splitlines():

                # We prepare our desired data fields and add
                # them to the data list.
                name, gender, count = line.split(",")
                data_list.append([year, name, gender, count])

    print("[{nowish}] data_list creation finished".format(
        nowish=prettytime()))

    # We save the data list into a csv file.
    csv.writer(open("data.csv", "w", newline="",
                    encoding="utf-8")).writerows(data_list)

    print("[{nowish}] csv written out".format(
        nowish=prettytime()))
