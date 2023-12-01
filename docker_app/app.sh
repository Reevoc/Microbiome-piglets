#!/bin/bash

echo START APP.SH

echo ACTIVATE ENVIRONMENT
source activate microbiome

cd /home/microbiome/docker_app/src/py
echo RUN ANALYSIS
python analysis.py

echo DEACTIVATE ENVIRONMENT
conda deactivate

