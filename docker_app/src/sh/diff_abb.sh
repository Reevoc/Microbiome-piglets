#!/bin/bash

cd /home/microbiome/

echo "START script for the computation of taxa barplot"
# Column ANCOM should be categorical
if [ $# -ne 4 ]; then
    echo "Usage: $0 <colum_name> <normalization> <metadata> <quantile>"
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

    # Run the Python script and capture the output
    output=$(python /home/microbiome/docker_app/src/py/extract_csv.py ${table} $2 $4)
    read sample_frequency feature_frequency <<< "$output"

    # Check and set minimum frequency if zero
    [ "$sample_frequency" -eq 0 ] && sample_frequency=1
    [ "$feature_frequency" -eq 0 ] && feature_frequency=1

    # Use sample_frequency and feature_frequency in your script
    echo "Sample Frequency: $sample_frequency"
    echo "Feature Frequency: $feature_frequency"

    mkdir -p "data/13.${number}_${table}_$2_DA_ANCOM"

    qiime feature-table filter-samples \
    --i-table data/10.${number}_${table}_${2}_table_norm/${table}_${2}_table_norm.qza \
    --p-min-frequency $sample_frequency \
    --o-filtered-table data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_sample_filtered.qza
    
    echo "Filtering by sample frequency --> done"

    qiime feature-table filter-features \
    --i-table data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_sample_filtered.qza \
    --p-min-samples $feature_frequency \
    --o-filtered-table data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_sample_feature_filtered.qza

    echo "Filtering by feature frequency --> done"

    qiime composition add-pseudocount \
        --i-table data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_sample_feature_filtered.qza \
        --o-composition-table "data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_DA_ANCOM_composition.qza"
    echo "Adding pseudocount --> done"

    # create a qzv for the last file before lunching ancom 
    qiime feature-table summarize \
        --i-table "data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_sample_feature_filtered.qza" \
        --o-visualization "data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_DA_ANCOM_composition.qzv" \
        --m-sample-metadata-file "data/0.2_piglets_metadata/$3"
    
    qiime composition ancom \
       --i-table "data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_DA_ANCOM_composition.qza" \
       --m-metadata-file "data/0.2_piglets_metadata/$3" \
       --m-metadata-column $1 \
       --p-transform-function "clr" \
       --o-visualization "data/13.${number}_${table}_$2_DA_ANCOM/${table}_$2_DA_ANCOM.qzv"
    
    echo "ANCOM --> done"

done