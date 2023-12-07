#!/bin/bash

# https://docs.qiime2.org/2023.9/tutorials/metadata/

echo "START .qzv for the metadata files"

cd /home/microbiome/data/0.2_piglets_metadata/

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <name_metadata>"
    exit 1
fi

source activate microbiome

metadata_name="${1::-4}"

qiime metadata tabulate \
    --m-input-file ./${1} \
    --o-visualization ./${metadata_name}.qzv

echo "END script for the creation of .qzv for the metadata files"

