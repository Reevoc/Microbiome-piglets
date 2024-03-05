#!/bin/bash

cd /home/microbiome/

echo "--> START DIFFERENTIAL ABUNDANCE ANALYSIS ANCOM"

if [ $# -ne 5 ]; then
    echo "Usage: $0 <colum_name> <normalization> <metadata> <quantile> <taxa>"
    exit 1
fi

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

echo "--> SAMPLE FREQUENCY: $sample_frequency"
echo "--> FEATURE FREQUENCY: $feature_frequency"

mkdir -p "data/8.${number}_${5}_${2}_DA_ANCOM"
# y vs e

# --i-table data/5.${number}_${5}_table_taxafilt/${5}_table_taxafilt.qza \
# --p-where "diarrhea = 'e' OR diarrhea = 'y'" \
# --p-where "is_sow = 'n'" \
qiime feature-table filter-samples \
--i-table data/6.${number}_${5}_${2}_table_norm/${5}_${2}_table_norm.qza \
--p-min-frequency $sample_frequency \
--m-metadata-file data/0_piglets_metadata/$3 \
--o-filtered-table data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_filtered.qza

echo "--> FILTERING BY SAMPLE FREQUENCY"

qiime feature-table filter-features \
--i-table data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_filtered.qza \
--p-min-samples $feature_frequency \
--o-filtered-table data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_feature_filtered.qza

echo "--> FILTERING BY FEATURE FREQUENCY"

qiime composition add-pseudocount \
    --i-table data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_sample_feature_filtered.qza \
    --o-composition-table "data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM_composition.qza"

echo "--> ADDING PSEUDOCOUNTS"

echo "--> SUMMARIZING"

qiime composition ancom \
    --i-table "data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM_composition.qza" \
    --m-metadata-file "data/0_piglets_metadata/$3" \
    --m-metadata-column ${1} \
    --o-visualization "data/8.${number}_${5}_${2}_DA_ANCOM/${5}_${2}_DA_ANCOM.qzv"

echo "--> ANCOM FINISHED"

