import utility

sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/"
metadata_folder = "/home/microbiome/data/0.2_piglets_metadata/"
sh_metadata = "/home/microbiome/docker_app/src/sh/metadata.sh"
metdadata_py = "/home/microbiome/docker_app/src/py/metadata.py"

utility.create_metadata_files(metdadata_py)

metadata = utility.metadata_choice(metadata_folder)

taxa_type = utility.table_choice()

normalization = utility.normalization_choice()

utility.run_metadata(sh_metadata, metadata)

utility.run_normalization(sh_normalization, taxa_type, normalization, metadata)

utility.run_metrics(sh_metrics, taxa_type, normalization, metadata)
