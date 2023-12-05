#!/bin/bash

echo "START script for the computation of alpha and beta diversity metrics"

cd /home/microbiome/data/0.2_piglets_metadata/

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <name_metadata>"
    exit 1
fi

source activate microbiome

qiime tools import \
  --type 'FeatureTable[Frequency]' \
  --input-path ${1} \
  --output-path ${1}.qza

mkdir ./exported_${1}

qiime diversity core-metrics-phylogenetic \
    --i-table ${1}.qza \
    --p-sampling-depth 10000 \
    --m-metadata-file ${1} \
    --output-dir ./exported_${1}

qiime tools export \
    --input-path ./exported_${1}/faith_pd_vector.qza \
    --output-path ./exported_${1}/exported_faith_pd_vector

qiime metadata tabulate \
    --m-input-file ./exported_${1}/exported_faith_pd_vector/faith_pd_vector.qza \
    --o-visualization ./${1}.qzv
