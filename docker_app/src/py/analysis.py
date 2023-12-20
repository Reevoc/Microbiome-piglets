import utility

sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/"
sh_metadata = "/home/microbiome/docker_app/src/sh/metadata.sh"
sh_barplot = "/home/microbiome/docker_app/src/sh/barplot.sh"
sh_ancom = "/home/microbiome/docker_app/src/sh/Diff_Abundandances.sh"
metadata_folder = "/home/microbiome/data/0.2_piglets_metadata/"
metdadata_py = "/home/microbiome/docker_app/src/py/metadata.py"

utility.create_metadata_files(metdadata_py)

metadata = utility.metadata_choice(metadata_folder)

imputation = utility.imputation_choice()

normalization = utility.normalization_choice()

taxa_type = utility.table_choice()

utility.run_metadata(sh_metadata, metadata)

utility.run_normalization(
    sh_normalization, taxa_type, normalization, metadata, imputation
)

utility.run_metrics(sh_metrics, taxa_type, normalization, metadata)

ancom = utility.ANCOM_choice()

if ancom:
    utility.run_ANCOM(sh_ancom, normalization, metadata)

save = utility.save_analysis_performed_choice()

if save:
    utility.run_barplot(sh_barplot, normalization, metadata)
    utility.save_analysis_performed(metadata, normalization, taxa_type, imputation)
