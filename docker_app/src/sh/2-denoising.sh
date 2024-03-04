#!/bin/bash

cd /home/microbiome

source activate microbiome

if [ $# -ne 2 ]; then
    echo "Usage: $0 <quality_value> <metadata>"
    exit 1
fi

echo "--> START DENOISING"

quality_file="data/2_paired-end-demux-trimmed/quality_threshold_50%_${1}.csv"
if [ -f "$quality_file" ]; then
    while IFS=, read -r key left right
    do
        if [[ "$key" == "forward"* ]]; then
            forward_right=$right
            forward_left=$left
        elif [[ "$key" == "reverse"* ]]; then
            reverse_right=$right
            reverse_left=$left
        fi
    done < "$quality_file"
else
    echo "CSV file not found"
    exit 1
fi


echo "--> metadata: ${2}"
echo "--> quality value: ${1}"
echo "--> forward_left: $forward_left"
echo "--> forward_right: $forward_right"
echo "--> reverse_left: $reverse_left"
echo "--> reverse_right: $reverse_right"

rm -rf data/3_feature_tables
mkdir -p data/3_feature_tables

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs data/2_paired-end-demux-trimmed/paired-end-demux-trimmed.qza \
  --p-trim-left-f $forward_left \
  --p-trim-left-r $reverse_left \
  --p-trunc-len-f $forward_right \
  --p-trunc-len-r $reverse_right \
  --p-n-threads 10 \
  --o-table data/3_feature_tables/feature_table.qza \
  --o-representative-sequences data/3_feature_tables/feature_sequences.qza \
  --o-denoising-stats data/3_feature_tables/denoising_stats.qza

qiime feature-table summarize \
  --i-table data/3_feature_tables/feature_table.qza \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}" \
  --o-visualization data/3_feature_tables/feature_table.qzv

qiime feature-table tabulate-seqs \
  --i-data data/3_feature_tables/feature_sequences.qza \
  --o-visualization data/3_feature_tables/feature_sequences.qzv

qiime metadata tabulate \
  --m-input-file data/3_feature_tables/denoising_stats.qza \
  --o-visualization data/3_feature_tables/denoising_stats.qzv

conda deactivate

echo "--> END DENOISING"










