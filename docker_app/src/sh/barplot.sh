#!/bin/bash

cd /home/microbiome

echo "START script for the computation of taxa barplot"

if [ $# -ne 2 ]; then
    echo "Usage: $0 <normalization> <metadata>"
    exit 1
fi

# Activate the Qiime2 environment
source activate microbiome

# If the file exists, add it to the list
file_path="/home/microbiome/data/10.1_asv_${1}_table_norm/asv_${1}_table_norm.qza"
variable="asv"
new_variable="12.1"

# Loop through the input tables
mkdir -p "data/${new_variable}_${variable}_${1}_taxa_barplot"
echo "Processing $input_table"
qiime taxa barplot \
    --i-table $file_path \
    --i-taxonomy "data/4_taxonomy/taxonomy.qza" \
    --m-metadata-file "data/0.2_piglets_metadata/${2}" \
    --o-visualization "data/${new_variable}_${variable}_${1}_taxa_barplot/${variable}_${1}_taxa_barplot.qzv"

# Deactivate the Qiime2 environment
conda deactivate

echo "END script for the computation of taxa barplot"
