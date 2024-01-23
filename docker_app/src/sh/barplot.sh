#!/bin/bash

cd /home/microbiome

echo "--> START TAXA BARPLOT SCRIPT"

if [ $# -ne 2 ]; then
    echo "Usage: $0 <normalization> <metadata>"
    exit 1
fi

file_path="/home/microbiome/data/10.1_asv_${1}_table_norm/asv_${1}_table_norm.qza"
variable="asv"
new_variable="12.1"

mkdir -p "data/${new_variable}_${variable}_${1}_taxa_barplot"

source activate microbiome

qiime taxa barplot \
    --i-table $file_path \
    --i-taxonomy "data/4_taxonomy/taxonomy.qza" \
    --m-metadata-file "data/0_piglets_metadata/${2}" \
    --o-visualization "data/${new_variable}_${variable}_${1}_taxa_barplot/${variable}_${1}_taxa_barplot.qzv"

conda deactivate

echo "--> END TAXA BARPLOT SCRIPT"
