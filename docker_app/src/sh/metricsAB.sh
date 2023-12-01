#!/bin/bash

echo "START script for the computation of alpha and beta diversity metrics"

cd /home/microbiome/

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type>"
    exit 1
fi

source activate microbiome

case $1 in 
asv)
    echo "working on taxa level: $1"
    ;;
genus)
    echo "working on taxa level: $1"
    ;;
species)
    echo "working on taxa level: $1"
    ;;
*)
    echo "Invalid choice, accepted parameter values: asv genus species"
    exit 1
    ;;
esac

case $2 in 
gmpr)
    echo "working on normalization type: $2"
    ;;
crl)
    echo "working on normalization type: $2"
    ;;
*)
    echo "Invalid choice, accepted parameter values: gmpr crl"
    exit 1
    ;;
esac

# Compute ALPHA DIVERSITY ON PHYLOGENETIC-RELATED METRICS

# Check the value of $1 and assign the appropriate value to the variable
if [ "$1" == "asv" ]; then
    variable_new="11.1"
    variable="10.1"
elif [ "$1" == "genus" ]; then
    variable_new="11.2"
    variable="10.2"
elif [ "$1" == "species" ]; then
    variable_new="11.3"
    variable="10.3"
else
    echo "Invalid choice, accepted parameter values: asv genus species"
    exit 1
fi

metadata="piglets_metadata.tsv"

if [ "$1" == "asv" ];then
#-----------------------------------------------------------------------------------------------------------
echo "Compute ALPHA DIVERSITY ON PHYLOGENETIC-RELATED METRICS"
mkdir -p "data/${variable_new}_${1}_${2}_phylogeny"
echo "Creating directory --> data/${variable_new}_${1}_${2}_phylogeny"

qiime diversity alpha-phylogenetic \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/6_tree/tree.qza" \
--p-metric 'faith_pd' \
--o-alpha-diversity "data/${variable_new}_${1}_${2}_phylogeny/${1}_${2}_phylogeny.qza"

echo "FAITH on $1"
mkdir -p "data/${variable_new}_${1}_${2}_phylogeny_stats"
echo "Creating directory --> data/${variable_new}_${1}_${2}_phylogeny_stats"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_phylogeny/${1}_${2}_phylogeny.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_phylogeny_stats/${1}_${2}_phylogeny_stats.qzv"

echo "STATS FAITH on $1"
mkdir -p "data/${variable_new}_${1}_${2}_weighted_unifrac"
echo "Creating directory --> data/${variable_new}_${1}_${2}_weighted_unifrac_${2}"

qiime diversity beta-phylogenetic \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/6_tree/tree.qza" \
--p-metric 'weighted_unifrac' \
--o-distance-matrix "data/${variable_new}_${1}_${2}_weighted_unifrac/${1}_${2}_weighted_unifrac.qza"

echo "WEIGHTED UNIFRAC on $1"
mkdir -p "data/${variable_new}_${1}_${2}_unweighted_unifrac"
echo "Creating directory --> data/${variable_new}_${1}_${2}_unweighted_unifrac_${2}"

qiime diversity beta-phylogenetic \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--i-phylogeny "data/6_tree/tree.qza" \
--p-metric 'unweighted_unifrac' \
--o-distance-matrix "data/${variable_new}_${1}_${2}_unweighted_unifrac/${1}_${2}_unweighted_unifrac.qza"

echo "UNWEIGHTED UNIFRAC on $1"
mkdir -p "data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa"
echo "Creating directory --> data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa_${2}"

qiime diversity pcoa \
--i-distance-matrix "data/${variable_new}_${1}_${2}_weighted_unifrac/${1}_${2}_weighted_unifrac.qza" \
--o-pcoa "data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa/${1}_${2}_weighted_unifrac_pcoa.qza"

echo "WEIGHTED UNIFRAC PCoAs $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa"
echo "Creating directory --> data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa_${2}"

qiime diversity pcoa \
--i-distance-matrix "data/${variable_new}_${1}_${2}_unweighted_unifrac/${1}_${2}_unweighted_unifrac.qza" \
--o-pcoa "data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa/${1}_${2}_unweighted_unifrac_pcoa.qza"

echo "UNWEIGHTED UNIFRAC PCoAs $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa_emperor"
echo "Creating directory --> data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa_emperor_${2}"

qiime emperor plot \
--i-pcoa "data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa/${1}_${2}_weighted_unifrac_pcoa.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_weighted_unifrac_pcoa_emperor/${1}_${2}_weighted_unifrac_pcoa_emperor.qzv"

echo "WEIGHTED UNIFRAC EMPEROR on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa_emperor"
echo "Creating directory --> data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa_emperor_${2}"

qiime emperor plot \
--i-pcoa "data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa/${1}_${2}_unweighted_unifrac_pcoa.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_unweighted_unifrac_pcoa_emperor/${1}_${2}_unweighted_unifrac_pcoa_emperor.qzv"

echo "UNWEIGHTED UNIFRAC EMPEROR on $1_$2"
fi

#--------------------------------------------------------------------------------------------
mkdir -p "data/${variable_new}_${1}_${2}_pielou"
echo "Creating directory --> data/${variable_new}_${1}_${2}_pielou_${2}"
echo "Compute ALPHA DIVERSITY ON NON-PHYLOGENETIC-RELATED METRICS"

qiime diversity alpha \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--p-metric 'pielou_e' \
--o-alpha-diversity "data/${variable_new}_${1}_${2}_pielou/${1}_${2}_pielou.qza"

echo "PIELOU on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_richness"
echo "Creating directory --> data/${variable_new}_${1}_${2}_richness_${2}"

qiime diversity alpha \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--p-metric 'observed_features' \
--o-alpha-diversity "data/${variable_new}_${1}_${2}_richness/${1}_${2}_richness.qza"

echo "RICHNESS on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_pielou_stats"
echo "Creating directory --> data/${variable_new}_${1}_${2}_pielou_stats_${2}"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_pielou/${1}_${2}_pielou.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_pielou_stats/${1}_${2}_pielou_stats.qzv"

echo "STATS PIELOU on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_richness_stats"
echo "Creating directory --> data/${variable_new}_${1}_${2}_richness_stats_${2}"

qiime diversity alpha-group-significance \
--i-alpha-diversity "data/${variable_new}_${1}_${2}_richness/${1}_${2}_richness.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_richness_stats/${1}_${2}_richness_stats.qzv"

echo "STATS RICHNESS on $1_$2"
echo "beta diversity $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_jaccard"
echo "Creating directory --> data/${variable_new}_${1}_${2}_jaccard_${2}"

qiime diversity beta \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--p-metric 'jaccard' \
--o-distance-matrix "data/${variable_new}_${1}_${2}_jaccard/${1}_${2}_jaccard.qza"

echo "JACCARD on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_braycurtis"
echo "Creating directory --> data/${variable_new}_${1}_${2}_braycurtis_${2}"

qiime diversity beta \
--i-table "data/${variable}_${1}_${2}_table_norm/${1}_${2}_table_norm.qza" \
--p-metric 'braycurtis' \
--o-distance-matrix "data/${variable_new}_${1}_${2}_braycurtis/${1}_${2}_braycurtis.qza"

echo "BRAYCURTIS on $1_$2"
echo "beta PCoAs $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_jaccard_pcoa"
echo "Creating directory --> data/${variable_new}_${1}_${2}_jaccard_pcoa_${2}"

qiime diversity pcoa \
--i-distance-matrix "data/${variable_new}_${1}_${2}_jaccard/${1}_${2}_jaccard.qza" \
--o-pcoa "data/${variable_new}_${1}_${2}_jaccard_pcoa/${1}_${2}_jaccard_pcoa.qza"

echo "JACCARD PCoAs $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_braycurtis_pcoa"
echo "Creating directory --> data/${variable_new}_${1}_${2}_braycurtis_pcoa_${2}"

qiime diversity pcoa \
--i-distance-matrix "data/${variable_new}_${1}_${2}_braycurtis/${1}_${2}_braycurtis.qza" \
--o-pcoa "data/${variable_new}_${1}_${2}_braycurtis_pcoa/${1}_${2}_braycurtis_pcoa.qza"

echo "BRAYCURTIS PCoAs $1_$2"
echo "emperor $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_jaccard_pcoa_emperor"
echo "Creating directory --> data/${variable_new}_${1}_${2}_jaccard_pcoa_emperor_${2}"

qiime emperor plot \
--i-pcoa "data/${variable_new}_${1}_${2}_jaccard_pcoa/${1}_${2}_jaccard_pcoa.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_jaccard_pcoa_emperor/${1}_${2}_jaccard_pcoa_emperor.qzv"

echo "JACCARD EMPEROR on $1_$2"
mkdir -p "data/${variable_new}_${1}_${2}_braycurtis_pcoa_emperor"
echo "Creating directory --> data/${variable_new}_${1}_${2}_braycurtis_pcoa_emperor_${2}"

qiime emperor plot \
--i-pcoa "data/${variable_new}_${1}_${2}_braycurtis_pcoa/${1}_${2}_braycurtis_pcoa.qza" \
--m-metadata-file "data/0.2_piglets_metadata/${metadata}" \
--o-visualization "data/${variable_new}_${1}_${2}_braycurtis_pcoa_emperor/${1}_${2}_braycurtis_pcoa_emperor.qzv"

echo "BRAYCURTIS EMPEROR on $1"
echo "STOP script"
