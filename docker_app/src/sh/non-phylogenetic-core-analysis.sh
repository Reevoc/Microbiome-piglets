#!/bin/bash

echo "--> START ALPHA AND BETA DIVERSITY METRICS NON-PHYLOGENETIC-RELATED"

cd /home/microbiome/

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <sampling_depth>"
    exit 1
fi

if [ "$1" == "genus" ];then
variable_new="11.2"
variable="10.2"
elif [ "$1" == "species" ];then
variable_new="11.3"
variable="10.3"
fi

echo "--> TAXA TYPE: $1"
echo "--> NORMALIZATION TYPE: $2"
echo "--> METADATA: $3"
sampling_depth=$(printf "%.0f" "${4}")
echo "--> SAMPLING DEPTH: $sampling_depth"

if ! [[ $sampling_depth =~ ^[0-9]+$ ]]; then
    echo "--> ERROR: Sampling depth must be a non-negative integer."
fi

echo "--> COMPUTING ALPHA AND BETA DIVERSITY METRICS CORE METRICS NON-PHYLOGENETIC-RELATED"

source activate microbiome
rm -rf "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic"

qiime diversity core-metrics \
# freature table qza imputate 
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--output-dir "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic" \
--p-sampling-depth ${sampling_depth}

echo "--> ALPHA GROUP SIGNIFICANCE"

# qiime diversity alpha-group-significance \
# --i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith_pd_vector.qza" \
# --m-metadata-file "data/0_piglets_metadata/${3}" \
# --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith_pd_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/shannon_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/shannon_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/evenness_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/evenness_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/observed_features_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/observed_features_vector.qzv"

conda deactivate

cd data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/

echo "--> RENAMING FILES"

for file in *.qzv; do mv "$file" "${1}_${2}_${file}"; done
for file in *.qza; do mv "$file" "${1}_${2}_${file}"; done

echo "--> END ALPHA AND BETA DIVERSITY METRICS NON-PHYLOGENETIC-RELATED"
