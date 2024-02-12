#!/bin/bash

cd /home/microbiome

conda activate microbiome

if [ $# -ne 2 ]; then
    echo "Usage: $0 <quality_value> <metadata>"
    exit 1
fi

echo "--> START DENOISING"

quality_file="data/2_paired-end-demux-trimming/quality_threshold_50%_${1}.csv"
if [ -f "$quality_file" ]; then
    while IFS=, read -r key value
    do
        if [ "$key" = "forward" ]; then
            forward=$value
        elif [ "$key" = "reverse" ]; then
            reverse=$value
        fi
    done < "$quality_file"
else
    echo "CSV file not found"
    exit 1
fi

echo "metadata --> ${2}"f
echo "quality value --> ${1}"
echo "forward value for quality ${1} --> $forward"
echo "revere value for quality ${1} --> $reverse"

qiime dada2 denoise-paired \
  --i-demultiplexed-seqs data/2_paired-end-demux-trimmed/paired-end-demux-trimmed.qza \
  --p-trunc-len-f $forward \
  --p-trunc-len-r $reverse \
  --p-n-threads 0 \
  --o-table data/3_feature_tables/feature_table.qza \
  --o-representative-sequences data/3_feature_tables/feature_sequences.qza \
  --o-denoising-stats data/3_feature_tables/denoising_stats.qza

qiime feature-table summarize \
  --i-table data/3_feature_tables/feature_table.qza \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}.tsv" \
  --o-visualization data/3_feature_tables/feature_table.qzv

qiime feature-table tabulate-seqs \
  --i-data data/3_feature_tables/feature_sequences.qza \
  --o-visualization data/3_feature_tables/feature_sequences.qzv

# Tabulate metadata
qiime metadata tabulate \
  --m-input-file data/3_feature_tables/denoising_stats.qza \
  --o-visualization data/3_feature_tables/denoising_stats.qzv

conda deactivate

echo "--> END DENOISING"

echo "--> START IMPUTATION"
cd /home/microbiome/docker_app/src/R
Rscript "${2}"

echo "--> END IMPUTATION"

conda activate microbiomecovid

echo "--> CONVERTING .BIOM TO .QZA"

qiime tools import \
  --input-path data/3.1_feature_table_imp/feature_table_imp.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV100Format \
  --output-path data/3.1_feature_table_imp/feature_table_imp.qza

qiime tools import \
  --input-path data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV100Format \
  --output-path data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qza

qiime tools import \
  --input-path data/3.3_feature_table_imp_lng/feature_table_imp_lng.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV100Format \
  --output-path data/3.3_feature_table_imp_lng/feature_table_imp_lng.qza

echo "--> FINISHED CONVERTING TO .QZA"

qiime feature-table summarize \
  --i-table data/3.1_feature_table_imp/feature_table_imp.qza \
  --o-visualization data/3.1_feature_table_imp/feature_table_imp.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}.tsv"

qiime feature-table summarize \
  --i-table data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qza \
  --o-visualization data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}.tsv"

qiime feature-table summarize \
  --i-table data/3.3_feature_table_imp_lng/feature_table_imp_lng.qza \
  --o-visualization data/3.3_feature_table_imp_lng/feature_table_imp_lng.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}.tsv"










