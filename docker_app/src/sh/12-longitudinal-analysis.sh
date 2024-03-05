#!/bin/bash

echo "--> START LONGITUDINAL ANALYSIS"

cd /home/microbiome/

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metric_column>"
    exit 1
fi
json_file="/home/microbiome/docker_app/src/json/longitudinal.json"
if [ ! -f "$json_file" ]; then
    echo "JSON file not found at $json_file"
    exit 1
fi
id=$(jq -r '.id' "$json_file")
group=$(jq -r '.group' "$json_file")
longitudinal=$(jq -r '.longitudinal' "$json_file")

if [ "$1" == "genus" ];then
variable_new="11.2"
variable_vol="12.2"
variable="6.2"
variab="7.2"
phylo="non_phylogenetic"
elif [ "$1" == "species" ];then
variable_new="11.3"
variable_vol="12.3"
variable="6.3"
variab="7.3"
phylo="non_phylogenetic"
elif [ "$1" == "asv" ];then
variable_new="11.1"
variable_vol="12.1"
variable="6.1"
variab="7.1"
phylo="phylogenetic"
fi

echo "--> TAXA TYPE: $1"
echo "--> NORMALIZATION TYPE: $2"
echo "--> METRIC: $3"
echo "--> GROUP COLUMN: ${group}"
echo "--> LONGITUDINAL COLUMN: ${longitudinal}"
echo "--> ID COLUMN: ${id}"

qiime longitudinal linear-mixed-effects \
    --i-table "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${1}_${2}_table_relative_frequency.qza" \
    --m-metadata-file "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/updated_metadata.tsv" \
    --p-metric ${3} \
    --p-state-column ${longitudinal} \
    --p-individual-id-column ${id} \
    --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_linear-mixed-effects.qzv"

echo "--> LONGITUDINAL ANALYSIS FEATURE VOLATILITY"

echo "rm -rf data/${1}_${2}_${longitudinal}_volatility"

qiime longitudinal feature-volatility \
    --i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
    --m-metadata-file "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/updated_metadata.tsv" \
    --p-state-column ${longitudinal} \
    --p-individual-id-column ${id} \
    --p-n-estimators 10 \
    --p-random-state 17 \
    --output-dir "data/${variable_vol}_${1}_${2}_${longitudinal}_volatility/"

echo "--> LONGITUDINAL ANALYSIS NMIT"

#qiime longitudinal nmit \
#    --i-table "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${1}_${2}_table_relative_frequency.qza" \
#    --m-metadata-file "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/updated_metadata.tsv" \
#    --p-individual-id-column ${id} \
#    --p-corr-method "pearson" \
#    --o-distance-matrix "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_distance_matrix.qza" \
#
#echo "--> LONGITUDINAL ANALYSIS BETA GROUP SIGNIFICANCE"
#
#qiime diversity beta-group-significance \
#    --i-distance-matrix "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_distance_matrix.qza" \
#    --m-metadata-file "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/updated_metadata.tsv" \
#    --m-metadata-column "${group}" \
#    --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_distance_matrix.qzv" \
#
#echo "--> LONGITUDINAL ANALYSIS PCOA"
#
#qiime diversity pcoa \
#    --i-distance-matrix "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_distance_matrix.qza" \
#    --o-pcoa "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_pcoa.qza" \
#
#echo "--> LONGITUDINAL ANALYSIS EMPEROR PLOT"
#
#qiime emperor plot \
#    --i-pcoa "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_pcoa.qza" \
#    --m-metadata-file "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/updated_metadata.tsv" \
#    --o-visualization "data/${variable_new}_${1}_${2}_core_metrics_longitudinal/${3}_nmit_pcoa.qzv" \
#
