#!/bin/bash
echo "--> START app.sh FOR MICROBIOME ANALYSIS"
cd /home/microbiome/docker_app/src/py
source activate qiime2-amplicon-2023.9
python analysis.py
conda deactivate
echo "--> END app.sh FOR MICROBIOME ANALYSIS"

