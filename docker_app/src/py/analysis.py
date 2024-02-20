from utility import create_metadata_files
from choice import metadata_choice, ANCOM_choice, table_choice, normalization_choice, imputation_choice, MASLIN_choice, quality_value_choice, taxonomy_choice
from choice import taxonomy_calassification_choice, tree_creation_choice
from run import run_metadata, run_normalization, run_ANCOM, run_MASLIN, run_metrics, run_denoising, run_get_infromations

sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/"
sh_metadata = "/home/microbiome/docker_app/src/sh/metadata.sh"
sh_barplot = "/home/microbiome/docker_app/src/sh/barplot.sh"
sh_ancom = "/home/microbiome/docker_app/src/sh/diff_abb_ANCOM.sh"
sh_maslin = "/home/microbiome/docker_app/src/sh/diff_abb_MaAsLin2.sh"
metadata_folder = "/home/microbiome/data/0_piglets_metadata/"
metdadata_py = "/home/microbiome/docker_app/src/py/metadata.py"
sh_denoising = "/home/microbiome/docker_app/src/sh/denoising.sh"


# create_metadata_files(metdadata_py)
# 
# tree_creation_choice()
# 
# taxonomy_calassification_choice()

metadata = metadata_choice(metadata_folder)

# run_metadata(sh_metadata, metadata)

# quality_value = quality_value_choice()
# 
# run_denoising(sh_denoising, metadata, quality_value)
# 
# taxonomy_choice()
# 
imputation = imputation_choice()

normalization = normalization_choice()

taxa_type = table_choice()

# run_normalization(sh_normalization, taxa_type, normalization, metadata, imputation)

# run_get_infromations()

# run_metrics(sh_metrics, taxa_type, normalization, metadata)

ancom = ANCOM_choice()

if ancom:
    run_ANCOM(sh_ancom, taxa_type, normalization, metadata)

maslin = MASLIN_choice()

if maslin:
    run_MASLIN(sh_maslin, taxa_type, normalization, metadata)
