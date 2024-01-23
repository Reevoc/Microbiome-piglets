#!/bin/bash

cd /home/microbiome/docker_app/src/R/

echo "--> START MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"

# Rscript DA_MasLin2.R -taxa asv -norm clr -outcome n -tsv piglets_modified_small.tsv -list_random "is_sow,time,sex"

if [ $# -ne 3 ]; then
    echo "Usage: $0 <taxa> <normalization> <metadata> "
    exit 1
fi

Rscript DA_MasLin2.R -taxa $1 -norm $2 -outcome diarrhea -tsv $3 -list_random "is_sow,sex,time"

echo "--> END MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"



