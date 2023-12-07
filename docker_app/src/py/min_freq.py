from bs4 import BeautifulSoup
import sys
import subprocess

# 2 arguments are expected: the script name and the HTML file name
if len(sys.argv) != 3:
    print("Error: 2 argument is expected")
    sys.exit(1)

if sys.argv[1] == "asv":
    name = "asv"
    value = "1"
elif sys.argv[1] == "genus":
    name = "genus"
    value = "2"
elif sys.argv[1] == "species":
    name = "species"
    value = "3"

path = f"/home/microbiome/data/10.{value}_{name}_{sys.argv[2]}_table_norm/{name}_{sys.argv[2]}_table_norm_export/"
print(path)
path_html = path + "index.html"
print(path_html)

# Read the HTML file
with open(path_html, "r") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the minimum frequency value
minimum_frequency_tag = soup.find("th", string="Minimum frequency")
minimum_frequency_value = minimum_frequency_tag.find_next("td").text
minimum_frequency_value = minimum_frequency_value.replace(",", "")
# Calculate the 90% of the minimum frequency value
minimum_frequency_value = float(minimum_frequency_value)
minimum_frequency_value = minimum_frequency_value * 0.9
minimum_frequency_value = int(minimum_frequency_value)

# save this value in a txt file

with open(
    f"/home/microbiome/data/10.{value}_{name}_{sys.argv[2]}_table_norm/min_freq.txt",
    "w",
) as file:
    file.write(str(minimum_frequency_value))

# eliminate this folder path = f"/home/microbiome/data/10.{value}_{name}_{sys.argv[2]}_table_norm/10.{value}_{name}_{sys.argv[2]}_table_norm_export/

subprocess.run(["rm", "-r", path])
