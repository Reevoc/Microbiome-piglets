#!/bin/bash

echo START app.sh
source activate microbiome
cd /home/microbiome/docker_app/src/py
python analysis.py
conda deactivate
echo END app.sh

