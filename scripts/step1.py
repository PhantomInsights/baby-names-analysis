"""
Downloads the data in a zip file, reads its contents and generates a
new csv file with the fields we need.
"""

import requests
from zipfile import ZipFile
import pandas as pd


def download():
    """Downloads the dataset and saves it to disk."""

    url = "https://www.ssa.gov/oact/babynames/names.zip"

    with requests.get(url) as response:

        with open("names.zip", "wb") as temp_file:
            temp_file.write(response.content)


def parse_zip():
    """Reads the contents of the zip file and creates a csv file with them."""

    columns = ["name", "gender", "count", "year"]

    with ZipFile("names.zip") as zf:
        files = zf.namelist()
        files = [zf.open(file) for file in files if ".txt" in file]
        df = pd.concat(
            (pd.read_csv(f, names=columns).assign(Year=f.name[3:7]) for f in files)
        )
        df.to_csv("data.csv", index=False)


if __name__ == "__main__":
    download()
    parse_zip()()
