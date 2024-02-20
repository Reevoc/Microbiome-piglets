#!/bin/bash

echo "--> START ALPHA AND BETA DIVERSITY METRICS PHYLOGENETIC-RELATED"

cd /home/microbiome/

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <sampling_depth>"
    exit 1
fi

source activate microbiome

variable_new="7.1"
variable="4.1"
sampling_depth=$(printf "%.0f" "${4}")
echo "--> TAXA TYPE: $1"
echo "--> NORMALIZATION TYPE: $2"
echo "--> METADATA: $3"
echo "--> SAMPLING DEPTH: $sampling_depth"

if ! [[ $sampling_depth =~ ^[0-9]+$ ]]; then
    echo "Error: Sampling depth must be a non-negative integer."
fi

echo "--> COMPUTING ALPHA AND BETA DIVERSITY METRICS CORE METRICS PHYLOGENETIC-RELATED"

rm -rf "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic"

qiime diversity core-metrics-phylogenetic \
--i-table "data/${variable}_${1}_table/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/tree/rooted-tree.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--output-dir "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic" \
--p-sampling-depth ${sampling_depth}

echo "--> ALPHA GROUP SIGNIFICANCE"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith_pd_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith_pd_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/evenness_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/evenness_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/shannon_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/shannon_vector.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/observed_features_vector.qza" \
--m-metadata-file "data/0_piglets_metadata/${3}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/observed_features_vector.qzv"

qiime diversity alpha-rarefaction \
  --i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
  --i-phylogeny "data/tree/rooted-tree.qza" \
  --m-metadata-file "data/0_piglets_metadata/${3}" \
  --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/${1}_${2}_diversity_alpha_rerefaction.qzv" \
  --p-max-depth ${sampling_depth}

conda deactivate

cd data/${variable_new}_${1}_${2}_core_metrics_phylogenetic

for file in *.qzv; do mv "$file" "${1}_${2}_${file}"; done
for file in *.qza; do mv "$file" "${1}_${2}_${file}"; done

echo "END script for the computation of alpha and beta diversity metrics phylogenetic-related"


