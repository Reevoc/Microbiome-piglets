import utility

sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/"
sh_metadata = "/home/microbiome/docker_app/src/sh/metadata.sh"
sh_barplot = "/home/microbiome/docker_app/src/sh/barplot.sh"
sh_ancom = "/home/microbiome/docker_app/src/sh/diff_abb_ANCOM.sh"
sh_maslin = "/home/microbiome/docker_app/src/sh/diff_abb_MaAsLin2.sh"
metadata_folder = "/home/microbiome/data/0_piglets_metadata/"
metdadata_py = "/home/microbiome/docker_app/src/py/metadata.py"

""" 
Launch the metadata.py script to create the different 
    metadata files specified in the file will store them inside the
    0_piglets_metadata folder
"""
# utility.create_metadata_files(metdadata_py)

"""
    Launch the metadata.sh script to choose one of the different
    metadata files created by the metadata.py script 
"""
metadata = utility.metadata_choice(metadata_folder)

"""
    Launch the run metadata.sh script to create the visualization
    for the metadata chosen by the user inside the folder 
    0_piglets_metadata
"""
# utility.run_metadata(sh_metadata, metadata)

"""
    Choose the type of the imputation to use for the later normalization
    there are avariable 3 different types of imputation:
    - raw
    - log_imputed
    - norm_imputed
"""
imputation = utility.imputation_choice()


"""
    Choose the type of normalization to use for the analysis
    There are 2 different types of normalization:
    - gmpr
    - clr
"""
normalization = utility.normalization_choice()


"""
    Choose the type of taxa to use for the analysis
    There are 3 different types of taxa:
    - species
    - genus
    - asv
"""
taxa_type = utility.table_choice()

"""
    Launch the normalization.sh script to normalize the data
    with the normalization and taxatype chosen by the user
"""
utility.run_normalization(
   sh_normalization, taxa_type, normalization, metadata, imputation
)

"""
    Launch the metrics.sh script to choose the metrics to use for the analysis
    there are 2 different type of metrics:
    - alpha
    - beta
    and are perforemed on phylogenetic and non-phylogenetic data
"""
utility.run_metrics(sh_metrics, taxa_type, normalization, metadata)

"""
    Decide if perform ancom analysis or not
"""
ancom = utility.ANCOM_choice()

"""
    If Yes, launch the ancom.sh script to perform the analysis
    it's also possible to choose the quantile to filter the data
    during the analysis
"""
if ancom:
    utility.run_ANCOM(sh_ancom, taxa_type, normalization, metadata)

"""
    Choose if perform MaAsLin2 analysis or not
"""
maslin = utility.MASLIN_choice()

"""
    If Yes, launch the maslin.sh script to perform the analysis
    TODO: add the possibility to choose the random and fixed effects
"""
if maslin:
    utility.run_MASLIN(sh_maslin, taxa_type, normalization, metadata)

# save = utility.save_analysis_performed_choice()
#
# if save:
#     utility.run_barplot(sh_barplot, normalization, metadata)
#     utility.save_analysis_performed(metadata, normalization, taxa_type, imputation)
