#!/bin/bash

cd /home/microbiome

source activate microbiome

echo "--> START GENERATE TREE"

qiime feature-classifier classify-sklearn \
--i-classifier data/classifier/classifier.qza \
--i-reads data/3_feature_tables/feature_sequences.qza \
--o-classification data/taxonomy/taxonomy.qza

qiime metadata tabulate \
--m-input-file data/taxonomy/taxonomy.qza \
--o-visualization data/taxonomy/taxonomy.qzv

conda deactivate


