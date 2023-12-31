#!/bin/bash

echo "START script for the computation of alpha and beta diversity metrics non-phylogenetic-related"

source activate microbiome

cd /home/microbiome/

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <sampling_depth>"
    exit 1
fi

source activate microbiome

# Compute ALPHA DIVERSITY ON NON-PHYLOGENETIC-RELATED METRICS
if [ "$1" == "genus" ];then
variable_new="11.2"
variable="10.2"
elif [ "$1" == "species" ];then
variable_new="11.3"
variable="10.3"
fi

metadata="$3"

echo "metadata: $metadata"

# Convert the sampling depth to an integer
sampling_depth=$(printf "%.0f" "${4}")
echo "sampling_depth: $sampling_depth"

# Check if the sampling depth is a non-negative integer
if ! [[ $sampling_depth =~ ^[0-9]+$ ]]; then
    echo "Error: Sampling depth must be a non-negative integer."
    exit 1
fi

# Perform core-metrics analysis
echo "Compute ALPHA and BETA DIVERSITY using core-metrics"

# Remove the output directory if it already exists
rm -rf "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic"

qiime diversity core-metrics \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--output-dir "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic" \
--p-sampling-depth ${sampling_depth}

# Alpha diversity group significance analysis
echo "Analyzing Alpha Diversity Group Significance"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/shannon_vector.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/shannon_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/evenness_vector.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/evenness_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/observed_features_vector.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/observed_features_vector.qzv"
conda deactivate



cd data/${variable_new}_${1}_${2}_core_metrics_non-phylogenetic/

for file in *.qzv; do mv "$file" "${1}_${2}_${file}"; done
for file in *.qza; do mv "$file" "${1}_${2}_${file}"; done

echo "END script for the computation of alpha and beta diversity metrics non-phylogenetic-related"
