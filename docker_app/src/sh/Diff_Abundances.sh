#!/bin/bash

cd /home/microbiome/data

echo "START script for the computation of taxa barplot"

if [ $# -ne 4 ]; then
    echo "Usage: $0 <col_name> <sample_name> <normalization> <metadata>"
    exit 1
fi

# Activate the Qiime2 environment
# Ensure that this works as expected in your setup
source activate microbiome

list_table=("asv" "genus" "species")
list_number=("1" "2" "3")

# Assuming the length of both lists is the same
for i in "${!list_table[@]}"; do
    table=${list_table[$i]}
    number=${list_number[$i]}

    mkdir -p "13.${number}_${table}_$3_$4_DA_ANCOM"

    qiime feature-table filter-samples \
      --i-table "/10.${number}_${table}_$2_norm" \
      --m-metadata-file "/0.2_piglets_metadata/$4" \
      --p-where "[$1]='${2}'" \
      --o-filtered-table "/13.${number}_${table}_$3_$4_DA_ANCOM/${table}_$3_$4_DA_ANCOM.qza"

    qiime composition add-pseudocount \
        --i-table "/13.${number}_${table}_$3_$4_DA_ANCOM/${table}_$3_$4_DA_ANCOM.qza" \
        --o-composition-table "/13.${number}_${table}_$3_$4_DA_ANCOM/${table}_$3_$4_DA_ANCOM_composition.qza"

    qiime composition ancom \
        --i-table "/13.${number}_${table}_$3_$4_DA_ANCOM/${table}_$3_$4_DA_ANCOM_composition.qza" \
        --m-metadata-file "/0.2_piglets_metadata/$4" \
        --m-metadata-column $1 \
        --o-visualization "/13.${number}_${table}_$3_$4_DA_ANCOM/${table}_$3_$4_DA_ANCOM.qzv"
done
