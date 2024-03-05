#!/bin/bash

echo "--> START EXTRACTING TSV FOR LONGITUDINAL ANALYSIS"

cd /home/microbiome/

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type>"
    exit 1
fi

if [ "$1" == "genus" ];then
variable_new="11.2"
variable="6.2"
variab="7.2"
phylo="non-phylogenetic"
elif [ "$1" == "species" ];then
variable_new="11.3"
variable="6.3"
variab="7.3"
phylo="non-phylogenetic"
elif [ "$1" == "asv" ];then
variable_new="11.1"
variable="6.1"
variab="7.1"
phylo="phylogenetic"
fi

echo "--> TAXA TYPE: $1"
echo "--> NORMALIZATION TYPE: $2"
echo "--> METADATA: $3"

rm -rf "data/${variable_new}_${1}_${2}_core_metrics_longitudinal"
mkdir -p "data/${variable_new}_${1}_${2}_core_metrics_longitudinal"

echo "--> CONVERT INTO RELATIVE FREQUENCY"

qiime feature-table relative-frequency \
    --i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
    --o-relative-frequency-table "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${1}_${2}_table_relative_frequency.qza"

echo "--> LONGITUDINAL ANALYSIS LME"

echo "--> EXPORT FROM SHANNON .QZA"

qiime tools export \
    --input-path "data/${variab}_${1}_${2}_core_metrics_${phylo}/${1}_${2}_shannon_vector.qza" \
    --output-path "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/"

echo "--> RENAME THE alpha-diversity.tsv in shannon_entropy.tsv"

mv "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/alpha-diversity.tsv" "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/shannon_entropy.tsv"

echo "--> EXPORT FROM OBSERVED FEATURES .QZA"

qiime tools export \
    --input-path "data/${variab}_${1}_${2}_core_metrics_${phylo}/${1}_${2}_observed_features_vector.qza" \
    --output-path "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/"

echo "--> RENAME THE alpha-diversity.tsv in observed_features.tsv" 

mv "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/alpha-diversity.tsv" "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/observed_features.tsv"

echo "--> EXPORT FROM EVENNESS .QZA"

qiime tools export \
    --input-path "data/${variab}_${1}_${2}_core_metrics_${phylo}/${1}_${2}_evenness_vector.qza" \
    --output-path "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/"

echo "--> RENAME THE alpha-diversity.tsv in pielou_evenness.tsv"

mv "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/alpha-diversity.tsv" "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/pielou_evenness.tsv"

if [ "$1" == "asv" ]; then

echo "--> EXPORT FROM FAITH PD .QZA"

qiime tools export \
    --input-path "data/${variab}_${1}_${2}_core_metrics_${phylo}/${1}_${2}_faith_pd_vector.qza" \
    --output-path "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/"

echo "--> EXPORT FROM FAITH PD .QZA"

mv "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/alpha-diversity.tsv" "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/faith_pd.tsv"

fi
