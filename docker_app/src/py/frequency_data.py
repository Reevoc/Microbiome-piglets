from bs4 import BeautifulSoup
import sys
import csv
import subprocess
from utility import extract_qzv_files, eliminate_subfolder, find_latest_directory

def read_and_parse_html(path_html):
    """Read and parse the HTML file."""
    try:
        with open(path_html, "r") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
        return soup
    except FileNotFoundError:
        print(f"File not found: {path_html}")
        sys.exit(2)

def extract_frequency_data(soup, section_title):
    """Extract frequency data from the specified section."""
    section = soup.find("h1", string=section_title)
    table = section.find_next("table")
    data = []
    for row in table.find_all("tr"):
        if row.find("th") is None or row.find("td") is None:
            continue
        data.append([row.find("th").text, row.find("td").text])
    return data

def write_to_csv(filename, data):
    """Write the extracted data to a CSV file."""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except IOError as e:
        print(f"Error writing file {filename}: {e}")
        sys.exit(3)

def main():
    if len(sys.argv) != 3:
        print("Error: 2 arguments are expected")
        sys.exit(1)

    name_mapping = {"asv": "1", "genus": "2", "species": "3"}
    name = sys.argv[1]
    if name not in name_mapping:
        print(f"Invalid name: {name}")
        sys.exit(4)
    normalization = sys.argv[2]
    value = name_mapping[name]
    base_path = "/home/microbiome/data"
    paths = {
        "path_1": f"{base_path}/4.{value}_{name}_table/",
        "path_2": f"{base_path}/5.{value}_{name}_table_taxafilt/",
        "path_3": f"{base_path}/6.{value}_{name}_{normalization}_table_norm/"
    }
    soups = {}
    for key in paths:
        extract_qzv_files(paths[key])
        directory_name = find_latest_directory(paths[key])
        path_html = f"{paths[key]}{directory_name}/data/index.html"        
        soups[key] = read_and_parse_html(path_html)


    sample_data = {key: extract_frequency_data(soup, "Frequency per sample") for key, soup in soups.items()}
    feature_data = {key: extract_frequency_data(soup, "Frequency per feature") for key, soup in soups.items()}


    combined_data = {}
    for key in paths:
        combined_data[key] = [["Metric", "Frequency Sample", "Frequency Feature"]]
        combined_data[key] += [
            [sample_row[0], sample_row[1], feature_row[1]]
            for sample_row, feature_row in zip(sample_data[key], feature_data[key])
        ]

    for key in paths:
        print(f"Writing to {paths[key]}summary.csv")
        write_to_csv(f"{paths[key]}summary.csv", combined_data[key])
        eliminate_subfolder(paths[key])

if __name__ == "__main__":
    main()
