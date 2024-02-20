#!/bin/bash

cd /home/microbiome/docker_app/src/R/

echo "--> START MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"

if [ $# -ne 3 ]; then
    echo "Usage: $0 <taxa> <normalization> <metadata> "
    exit 1
fi

Rscript DA_MasLin2.R -taxa $1 -norm $2 -outcome diarrhea -tsv $3 -list_random "" -column_name "diarrhea" -list_column_value "y,n,e"

echo "--> END MaAsLin2 DIFFERENTIAL ABUNDANCE ANALYSIS"
