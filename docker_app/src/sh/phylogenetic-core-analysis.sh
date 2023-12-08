#!/bin/bash

echo "START script for the computation of alpha and beta diversity metrics pylogenetic-related"

cd /home/microbiome/

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <sampling_depth>"
    exit 1
fi

source activate microbiome

case $1 in 
asv)
    echo "CORRECT WORKING IN PHYLOGENETIC ANALYSIS ON ASV LVL: $1"
    ;;
genus)
    echo "ERROR WORKING IN PHYLOGENETIC ANALYSIS ON GENUS LEVEL"
    ;;
species)
    echo "ERROR WORKING IN PHYLOGENETIC ANALYSIS ON SPECIES LEVEL"
    ;;
*)
    echo "Invalid choice, accepted parameter values: asv genus species"
    exit 1
    ;;
esac

# Compute ALPHA DIVERSITY ON PHYLOGENETIC-RELATED METRICS
variable_new="11.1"
variable="10.1"
metadata="$3"

# Convert the sampling depth to an integer
sampling_depth=$(printf "%.0f" "${4}")
echo "sampling_depth: $sampling_depth"

# Check if the sampling depth is a non-negative integer
if ! [[ $sampling_depth =~ ^[0-9]+$ ]]; then
    echo "Error: Sampling depth must be a non-negative integer."
    exit 1
fi

echo "metadata: $metadata"

# Perform core-metrics-phylogenetic analysis
echo "Compute ALPHA and BETA DIVERSITY using core-metrics-phylogenetic"

# Remove the output directory if it already exists
rm -rf "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic"

qiime diversity core-metrics-phylogenetic \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/6_tree/tree.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--output-dir "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic" \
--p-sampling-depth ${sampling_depth}

qiime diversity alpha-rarefaction \
  --i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
  --i-phylogeny "data/6_tree/tree.qza" \          
  --m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
  --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_phylogenetic/${1}_${2}_diversity_alpha_rerefaction.qzv" \
  --p-max-depth 4000 
echo  "END script for the computation of alpha and beta diversity metrics pylogenetic-related"

conda deactivate