echo View app activated

source /home/piermarco/miniconda3/bin/activate qiime2-amplicon-2023.9

echo conda environment activated

cd /home/piermarco/Documents/Thesis/view

python3 view.py

conda deactivate

echo View app deactivated
