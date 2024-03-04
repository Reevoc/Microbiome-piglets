#!/bin/bash

echo "--> START NORMALIZATION SCRIPT"

cd /home/microbiome

source activate microbiome

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <taxa_type> <normalization_type> <metadata> <imputation>"
    exit 1
fi

case $1 in
species)
    pL=7
    echo "--> TAXA TYPE:$1 "
    echo "--> PRUNING LEVEL: $pL"
    ;;

genus)
    pL=6
    echo "--> TAXA TYPE: $1 "
    echo "--> PRUNING LEVEL: $pL"
    ;;

asv)
    echo "--> TAXA TYPE: $1"
    ;;

*)
    echo "--> ERROR: Invalid choice, accepted parameter values: asv genus species"
    ;;
esac

case $2 in
gmpr)
    echo "--> NORMALIZATION: $2"
    ;;
clr)
    echo "--> NORMALIZATION: $2"
    ;;
*)
    echo "--> ERROR Invalid choice, accepted parameter values: gmpr clr"
    ;;
esac

echo "--> METADATA: $3"

echo "--> IMPUTATION: $4"

if [ "$1" == "asv" ]; then
variable="1"
elif [ "$1" == "genus" ]; then
variable="2"
elif [ "$1" == "species" ]; then
variable="3"
else
echo "--> ERROR Invalid choice, accepted parameter values: asv genus species"
fi

if [ "$4" == "feature_table_imp" ]; then
imp="1"
elif [ "$4" == "feature_table_imp_nrm" ]; then
imp="2"
elif [ "$4" == "feature_table_imp_lgn" ]; then
imp="3"
else
echo "Invalid choice, accepted parameter values: feature_table_imp feature_table_imp_nrm feature_table_imp_lgn"
fi

mkdir -p data/4.${variable}_$1_table

if [ "$1" == "asv" ]; then

    echo "--> NO COLLAPSING $1_table.qza"
    
    cp data/3.${imp}_${4}/${4}.qza data/4.${variable}_$1_table/$1_table.qza

    qiime feature-table summarize \
        --i-table data/4.${variable}_$1_table/$1_table.qza \
        --o-visualization data/4.${variable}_$1_table/$1_table.qzv \
        --m-sample-metadata-file data/0_piglets_metadata/$3

else

    echo "--> COLLAPSING $1"
    qiime taxa collapse \
        --i-table data/3.${imp}_${4}/${4}.qza \
        --i-taxonomy data/taxonomy/taxonomy.qza \
        --p-level ${pL} \
        --o-collapsed-table data/4.${variable}_$1_table/$1_table.qza

    qiime feature-table summarize \
        --i-table data/4.${variable}_$1_table/$1_table.qza \
        --o-visualization data/4.${variable}_$1_table/$1_table.qzv \
        --m-sample-metadata-file data/0_piglets_metadata/$3 
fi

echo "--> COLLAPSED TO $1_table.qza" 

rm -rf data/5.${variable}_$1_table_taxafilt
mkdir -p data/5.${variable}_$1_table_taxafilt

    qiime feature-table filter-features \
        --i-table data/4.${variable}_$1_table/$1_table.qza \
        --p-min-frequency 1 \
        --o-filtered-table data/5.${variable}_$1_table_taxafilt/$1_table_taxafilt.qza
    echo "--> FILTERED TO: $1_table_taxafilt.qza"

    qiime feature-table summarize \
        --i-table data/5.${variable}_$1_table_taxafilt/$1_table_taxafilt.qza \
        --o-visualization data/5.${variable}_$1_table_taxafilt/$1_table_taxafilt.qzv \
        --m-sample-metadata-file data/0_piglets_metadata/$3

conda deactivate

rm -rf data/6.${variable}_$1_$2_table_norm
mkdir -p data/6.${variable}_$1_$2_table_norm

if [ "$2" == "gmpr" ]; then
    echo "--> LAUNCHING GMPR"
    Rscript docker_app/src/R/GMPR_TRY.R $1
fi

if [ "$2" == "clr" ]; then
    echo "--> LAUNCHING CLR"
    Rscript docker_app/src/R/CLR.R $1
fi

source activate microbiome

echo "--> CONVERTING $1_table_norm.biom to $1_$2_table_norm.qza"

    qiime tools import \
        --input-path data/6.${variable}_$1_$2_table_norm/$1_$2_table_norm.biom \
        --type 'FeatureTable[Frequency]' \
        --input-format BIOMV100Format \
        --output-path data/6.${variable}_$1_$2_table_norm/$1_$2_table_norm.qza
    echo "--> CONVERTED IN $1_$2_table_norm.qza"
    
echo "--> SUMMARIZING $1_$2_table_norm.qza"

qiime feature-table summarize \
    --i-table data/6.${variable}_$1_$2_table_norm/$1_$2_table_norm.qza \
    --o-visualization data/6.${variable}_$1_$2_table_norm/$1_$2_table_norm.qzv \

echo "--> SUMMARIZED IN $1_$2_table_norm.qzv"

conda deactivate

echo "--> LAUNCH PYTHON SCRIPT FOR FREQUENCY DATA"

cd /home/microbiome/docker_app/src/py
python3 frequency_data.py $1 $2 

echo "--> END NORMALIZATION SCRIPT"
