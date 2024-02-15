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


echo "metadata --> ${2}"
echo "quality value --> ${1}"
echo "forward_left --> $forward_left"
echo "forward_right --> $forward_right"
echo "reverse_left --> $reverse_left"
echo "reverse_right --> $reverse_right"


qiime dada2 denoise-paired \
  --i-demultiplexed-seqs data/2_paired-end-demux-trimmed/paired-end-demux-trimmed.qza \
  --p-trim-left-f $forward_left \
  --p-trim-left-r $reverse_left \
  --p-trunc-len-f $forward_right \
  --p-trunc-len-r $reverse_right \
  --p-n-threads 6 \
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
#
conda deactivate

echo "--> END DENOISING"

echo "--> START IMPUTATION"

Rscript docker_app/src/R/mBImpute.R $2 

echo "--> END IMPUTATION"

source activate microbiome

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
  --input-path data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.biom \
  --type 'FeatureTable[Frequency]' \
  --input-format BIOMV100Format \
  --output-path data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.qza

echo "--> FINISHED CONVERTING TO .QZA"

qiime feature-table summarize \
  --i-table data/3.1_feature_table_imp/feature_table_imp.qza \
  --o-visualization data/3.1_feature_table_imp/feature_table_imp.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}"

qiime feature-table summarize \
  --i-table data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qza \
  --o-visualization data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}"

qiime feature-table summarize \
  --i-table data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.qza \
  --o-visualization data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${2}"

conda deactivate









