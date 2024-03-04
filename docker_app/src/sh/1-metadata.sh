#!/bin/bash

echo "--> START METADATA SCRIPT"

cd /home/microbiome/data/0_piglets_metadata/

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <name_metadata>"
    exit 1
fi

source activate microbiome

metadata_name="${1::-4}"

qiime metadata tabulate \
    --m-input-file ./${1} \
    --o-visualization ./${metadata_name}.qzv

conda deactivate

echo "--> END METADATA SCRIPT"

