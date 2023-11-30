#!/bin/bash

echo START APP.SH
cd /home/microbiome/src

echo ACTIVATE ENVIRONMENT
source activate microbiome

echo UNIZP ARCHIVE
unzip /home/microbiome/data.zip -d /home/microbiome/

echo RUN ANALYSIS
python3 analysis.py

echo DEACTIVATE ENVIRONMENT
conda deactivate

