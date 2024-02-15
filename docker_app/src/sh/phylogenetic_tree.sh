#!/bin/bash

cd /home/microbiome

echo "--> PHYLOGENETIC TREE SCRIPT"

source activate microbiome

qiime phylogeny align-to-tree-mafft-fasttree \
--i-sequences data/3_feature_tables/feature_sequences.qza \
--o-alignment data/tree/aligned-rep-seqs.qza \
--o-masked-alignment data/tree/masked-aligned-rep-seqs.qza \
--o-tree data/tree/unrooted-tree.qza \
--o-rooted-tree data/tree/rooted-tree.qza

conda deactivate

echo "--> PHYLOGENETIC TREE SCRIPT FINISHED"
