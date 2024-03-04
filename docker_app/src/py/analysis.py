from utility import create_metadata_files
from choice import metadata_choice, ANCOM_choice, table_choice, normalization_choice, imputation_choice, MASLIN_choice, quality_value_choice, taxonomy_choice
from choice import taxonomy_calassification_choice, tree_creation_choice
from run import run_metadata, run_normalization, run_ANCOM, run_MASLIN, run_metrics, run_denoising, run_get_infromations, run_intersecate_ANCOM_MaAsLin, run_imputation

# Path to the shell scripts
sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/"
sh_metadata = "/home/microbiome/docker_app/src/sh/1-metadata.sh"
sh_ancom = "/home/microbiome/docker_app/src/sh/diff_abb_ANCOM.sh"
sh_maslin = "/home/microbiome/docker_app/src/sh/diff_abb_MaAsLin2.sh"
sh_denoising = "/home/microbiome/docker_app/src/sh/2-denoising.sh"
sh_imputation = "/home/microbiome/docker_app/src/sh/4-imputation.sh"
# Folder where the metadata files are stored
metadata_folder = "/home/microbiome/data/0_piglets_metadata/"
metdadata_py = "/home/microbiome/docker_app/src/py/metadata.py"


#create_metadata_files(metdadata_py) # create the metadata files
metadata = metadata_choice(metadata_folder) # choice the metadata file to use
#run_metadata(sh_metadata, metadata) # create metadata.qzv 
#quality_value = quality_value_choice() # call the quality value for trimming
#run_denoising(sh_denoising, metadata, quality_value) # run the denoising.sh and the imputation method
#tree_creation_choice() # create the tree.qza file and the nwk files
#taxonomy_calassification_choice() # call the taxonomy calassification.sh
#taxonomy_choice()# create the taxonomy.tsv file
run_imputation(sh_imputation, metadata) # run the imputation.sh
imputation = imputation_choice() # choice the imputation method to use
normalization = normalization_choice() # choice the normalization method to use
taxa_type = table_choice() # choice the taxa type to use
run_normalization(sh_normalization, taxa_type, normalization, metadata, imputation) # run the normalization.sh
run_get_infromations() # get the informations from the normalization.qza file
run_metrics(sh_metrics, taxa_type, normalization, metadata) # run the metrics.sh alpha and beta diversity
ancom = ANCOM_choice() # choice if you want to run the ANCOM
if ancom:
    run_ANCOM(sh_ancom, taxa_type, normalization, metadata) # run the ANCOM.sh
maslin = MASLIN_choice() # choice if you want to run the MASLIN
if maslin:
    run_MASLIN(sh_maslin, taxa_type, normalization, metadata) # run the MASLIN.sh
run_intersecate_ANCOM_MaAsLin() # run the intersecate_ANCOM_MaAsLin.sh