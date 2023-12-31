#!/bin/bash

cd /home/microbiome/

echo "START script for the computation of taxa barplot"
# Column ANCOM should be categorical
if [ $# -ne 2 ]; then
    echo "Usage: $0 <colum_amom> <normalization> <metadata>"
    exit 1
fi

# Activate the Qiime2 environment
# Ensure that this works as expected in your setup
source activate microbiome

list_table=("asv" "genus" "species")
list_number=("1" "2" "3")

# Assuming the length of both lists is the same
for i in "${!list_table[@]}"; do
    echo "table: ${list_table[$i]}"
    table=${list_table[$i]}
    number=${list_number[$i]}
    mkdir -p "data/13.${number}_${table}_$3_DA_ANCOM"

    qiime feature-table filter-samples \
      --i-table "data/10.${number}_${table}_$3_table_norm/${table}_$3_table_norm.qza" \
      --m-metadata-file "data/0.2_piglets_metadata/$4" \
      --o-filtered-table "data/13.${number}_${table}_$3_DA_ANCOM/${table}_$3_DA_ANCOM.qza"
    
    echo "filtering done"

    qiime composition add-pseudocount \
        --i-table "data/13.${number}_${table}_$3_DA_ANCOM/${table}_$3_DA_ANCOM.qza" \
        --o-composition-table "data/13.${number}_${table}_$3_DA_ANCOM/${table}_$3_DA_ANCOM_composition.qza"
    
    echo "pseudocount done"
    
    qiime composition ancom \
       --i-table "data/13.${number}_${table}_$3_DA_ANCOM/${table}_$3_DA_ANCOM_composition.qza" \
       --m-metadata-file "data/0.2_piglets_metadata/$4" \
       --m-metadata-column $1 \
       --o-visualization "data/13.${number}_${table}_$3_DA_ANCOM/${table}_$3_DA_ANCOM.qzv"
    
    echo "ancom done"
done