#!/bin/bash

echo "--> START MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"
cd /home/microbiome/docker_app/src

# Check if correct number of command-line arguments are passed
if [ $# -ne 3 ]; then
    echo "Usage: $0 <taxa> <normalization> <metadata>"
    exit 1
fi

# Corrected path to match the exact filename and location
json_file="/home/microbiome/docker_app/src/json/maAslin2.json"
if [ ! -f "$json_file" ]; then
    echo "JSON file not found at $json_file"
    exit 1
fi

# Extract values from JSON file
outcome=$(jq -r '.outcome' "$json_file")
list_random=$(jq -r '.list_random' "$json_file")
column_name=$(jq -r '.column_name' "$json_file")
list_column_value=$(jq -r '.list_column_value' "$json_file")

# Change directory to where R script is located
cd /home/microbiome/docker_app/src/R

# Run the R script with parameters
Rscript DA_MasLin2.R -taxa $1 -norm $2 -outcome "$outcome" -tsv $3 -list_random "$list_random" -column_name "$column_name" -list_column_value "$list_column_value"

echo "--> END MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"
