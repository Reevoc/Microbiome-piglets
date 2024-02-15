from bs4 import BeautifulSoup
import sys
import csv
import subprocess

def read_and_parse_html(path_html):
    """Read and parse the HTML file."""
    with open(path_html, "r") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
    return soup

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
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    if len(sys.argv) != 3:
        print("Error: 2 arguments are expected")
        sys.exit(1)

    name_mapping = {"asv": "1", "genus": "2", "species": "3"}
    name = sys.argv[1]
    value = name_mapping.get(name, "1")

    path = f"/home/microbiome/data/6.{value}_{name}_{sys.argv[2]}_table_norm/{name}_{sys.argv[2]}_table_norm_export/"
    path_html = path + "index.html"

    soup = read_and_parse_html(path_html)

    sample_data = extract_frequency_data(soup, "Frequency per sample")
    feature_data = extract_frequency_data(soup, "Frequency per feature")

    combined_data = [["Metric", "Frequency Sample", "Frequency Feature"]]
    for sample_row, feature_row in zip(sample_data, feature_data):
        combined_data.append([sample_row[0], sample_row[1], feature_row[1]])

    csv_file = f"/home/microbiome/data/6.{value}_{name}_{sys.argv[2]}_table_norm/{name}_{sys.argv[2]}_summary.csv"
    write_to_csv(csv_file, combined_data)
    
    subprocess.run(["rm", "-r", path])


if __name__ == "__main__":
    main()
