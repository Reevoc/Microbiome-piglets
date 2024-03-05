#!/bin/bash
if [ $# -ne 3 ]; then
    echo "Usage: $0 <metadata> <usage_of_tree_yes_or_no> <tree_rooted_or_unrooted> "
    exit 1
fi

cd /home/microbiome
rm -rf data/3.1_feature_table_imp
rm -rf data/3.2_feature_table_imp_nrm
rm -rf data/3.3_feature_table_imp_lgn
mkdir -p data/3.1_feature_table_imp
mkdir -p data/3.2_feature_table_imp_nrm
mkdir -p data/3.3_feature_table_imp_lgn

echo "--> START IMPUTATION"

Rscript docker_app/src/R/mBImpute.R $1 $2 $3

echo "--> END IMPUTATION"



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
  --m-sample-metadata-file "data/0_piglets_metadata/${1}"

qiime feature-table summarize \
  --i-table data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qza \
  --o-visualization data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${1}"

qiime feature-table summarize \
  --i-table data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.qza \
  --o-visualization data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.qzv \
  --m-sample-metadata-file "data/0_piglets_metadata/${1}"


