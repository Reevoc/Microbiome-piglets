#!/bin/bash

cd /home/microbiome



echo "--> START TAXONOMY CLASSIFICATION"

rm -rf data/taxonomy
mkdir -p data/taxonomy

qiime feature-classifier classify-sklearn \
--i-classifier data/classifier/classifier.qza \
--i-reads data/3_feature_tables/feature_sequences.qza \
--o-classification data/taxonomy/taxonomy.qza

qiime metadata tabulate \
--m-input-file data/taxonomy/taxonomy.qza \
--o-visualization data/taxonomy/taxonomy.qzv




