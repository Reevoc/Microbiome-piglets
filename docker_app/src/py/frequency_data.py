from bs4 import BeautifulSoup
import sys
import csv
import subprocess

# Check for the correct number of arguments
if len(sys.argv) != 3:
    print("Error: 2 arguments are expected")
    sys.exit(1)

# Map command line arguments to folder names
name_mapping = {"asv": "1", "genus": "2", "species": "3"}
name = sys.argv[1]
value = name_mapping.get(name, "1")

# Construct the file paths
path = f"/home/microbiome/data/10.{value}_{name}_{sys.argv[2]}_table_norm/{name}_{sys.argv[2]}_table_norm_export/"
path_html = path + "index.html"

# Read and parse the HTML file
with open(path_html, "r") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

# Find the 'Frequency per sample' section and its corresponding table
freq_sample_section_sample = soup.find("h1", string="Frequency per sample")
freq_sample_table_sample = freq_sample_section_sample.find_next("table")
freq_sample_section_feature = soup.find("h1", string="Frequency per feature")
freq_sample_table_feature_feature = freq_sample_section_feature.find_next("table")
# Process the table and extract data
data = [["Metric", "Frequency Sample", "Frequency Feature"]]
for table_sample, table_feature in zip(
    freq_sample_table_sample.find_all("tr"),
    freq_sample_table_feature_feature.find_all("tr"),
):
    if (
        table_sample.find("th") is None
        or table_sample.find("td") is None
        or table_feature.find("td") is None
    ):
        continue

    data.append(
        [
            table_sample.find("th").text,
            table_sample.find("td").text,
            table_feature.find("td").text,
        ]
    )


# Write data to a CSV file
csv_file = f"/home/microbiome/data/10.{value}_{name}_{sys.argv[2]}_table_norm/{name}_{sys.argv[2]}_summary.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Optional: remove the folder
subprocess.run(["rm", "-r", path])
