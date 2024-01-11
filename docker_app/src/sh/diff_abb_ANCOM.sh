#!/bin/bash

cd /home/microbiome/

echo "START script for the computation of taxa barplot"


if [ $# -ne 5 ]; then
    echo "Usage: $0 <colum_name> <normalization> <metadata> <quantile> <taxa>"
    exit 1
fi

source activate microbiome

output=$(python /home/microbiome/docker_app/src/py/extract_csv.py ${5} ${2} ${4})
read sample_frequency feature_frequency <<< "$output"

if [ $5 == "asv" ];then
    number="1"
elif [ $5 == "genus" ];then
    number="2"
elif [ $5 == "species" ];then
    number="3"
else
    echo "Invalid choice, accepted parameter values: asv genus species"
fi

[ "$sample_frequency" -eq 0 ] && sample_frequency=1
[ "$feature_frequency" -eq 0 ] && feature_frequency=1

echo "Sample Frequency: $sample_frequency"
echo "Feature Frequency: $feature_frequency"

mkdir -p "data/13.${number}_${5}_${2}_DA_ANCOM"

qiime feature-table filter-samples \
--i-table data/10.${number}_${5}_${2}_table_norm/${5}_${2}_table_norm.qza \
--p-min-frequency $sample_frequency \
--o-filtered-table data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_filtered.qza

echo "Filtering by sample frequency --> done"

qiime feature-table filter-features \
--i-table data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_filtered.qza \
--p-min-samples $feature_frequency \
--o-filtered-table data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_feature_filtered.qza

echo "Filtering by feature frequency --> done"

qiime composition add-pseudocount \
    --i-table data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_feature_filtered.qza \
    --o-composition-table "data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM_composition.qza"
echo "Adding pseudocount --> done"

qiime feature-table summarize \
    --i-table "data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_feature_filtered.qza" \
    --o-visualization "data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM_composition.qzv" \
    --m-sample-metadata-file "data/0.2_piglets_metadata/$3"

qiime composition ancom \
    --i-table "data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM_composition.qza" \
    --m-metadata-file "data/0.2_piglets_metadata/$3" \
    --m-metadata-column ${1} \
    --p-transform-function "clr" \
    --o-visualization "data/13.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM.qzv"

echo "ANCOM --> done"

