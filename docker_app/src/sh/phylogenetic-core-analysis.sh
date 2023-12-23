#!/bin/bash

echo "START script for the computation of alpha and beta diversity metrics phylogenetic-related"

cd /home/microbiome/

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <sampling_depth>"
    exit 1
fi

source activate microbiome

variable_new="11.1"
variable="10.1"
metadata="$3"

sampling_depth=$(printf "%.0f" "${4}")
echo "taxa type --> $1"
echo "normalization type --> $2"
echo "metadata --> $metadata"
echo "sampling_depth --> $sampling_depth"

if ! [[ $sampling_depth =~ ^[0-9]+$ ]]; then
    echo "Error: Sampling depth must be a non-negative integer."
    exit 1
fi

echo "metadata: $metadata"

echo "Compute ALPHA and BETA DIVERSITY using core-metrics-phylogenetic"

rm -rf "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic"

qiime diversity core-metrics-phylogenetic \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/6_tree/tree.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--output-dir "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic" \
--p-sampling-depth ${sampling_depth}

# Alpha diversity group significance analysis
echo "Analyzing Alpha Diversity Group Significance"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith_pd_vector.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/faith-pd-group-significance.qzv"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/evenness_vector.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/evenness-group-significance.qzv"

qiime diversity alpha-rarefaction \
  --i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
  --i-phylogeny "data/6_tree/tree.qza" \
  --m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
  --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/${1}_${2}_diversity_alpha_rerefaction.qzv" \
  --p-max-depth ${sampling_depth}

echo "END script for the computation of alpha and beta diversity metrics phylogenetic-related"

conda deactivate
