import subprocess
import pandas as pd
from message import print_message, print_explanation
from choice import column_for_ancom_choice, quantile_choice
from utility import read_quantile


def run_denoising(path_denosing_sh, metadata_file, quality_value):
    """
    Run the denoising the denoising
    """
    print(f"bash {path_denosing_sh} {quality_value} {metadata_file}")
    subprocess.run(["bash", path_denosing_sh, str(quality_value), metadata_file])
    
def run_ANCOM(sh_ANCOM, taxa_type, normalization, metadata_file):
    """Run ANCOM analysis."""
    path_metadata = f"/home/microbiome/data/0_piglets_metadata/{metadata_file}"
    metadata_df = pd.read_csv(path_metadata, sep="\t")
    col_name = column_for_ancom_choice(metadata_df)
    taxa_list = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
    normalizations = ["gmpr", "clr"] if normalization == "all" else [normalization]
    print_message(
        "ATTENTION: using ANCOM with clr, ANCOM perform automatically a CLR in output\n"
        + "so if you use clr as normalization you will have a double CLR in output.\n"
        + "Instead is better if only check the output of ANCOM with gmpr normalization\n"
        + "ATTENTION to the usage of the min frequency for the quantile in ASV table\n"
        + "cause long time of analysis, for the output of .qzv file\n"
    )
    for norm in normalizations:
        for taxa in taxa_list:
            print_message(f"ANCOM for {taxa} {norm} data")
            quantile_num = quantile_choice()
            try:
                subprocess.run(
                    [
                        "bash",
                        sh_ANCOM,
                        col_name,
                        norm,
                        metadata_file,
                        quantile_num,
                        taxa,
                    ]
                )
            except subprocess.CalledProcessError:
                print_message("\nError during ANCOM bash launch\n")


def run_MASLIN(sh_MASLIN, taxa_type, normalization, metadata_file):
    """Run MaAsLin2 analysis."""
    path_to_data = '/home/microbiome/data/'
    subprocess.run(['bash', '-c', f'find {path_to_data} -name "14*" -exec rm -rf {{}} +'])
    taxa_types = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
    normalizations = ["gmpr", "clr"] if normalization == "all" else [normalization]
    for norm in normalizations:
        for taxa in taxa_types:
            try:
                subprocess.run(["bash", sh_MASLIN, taxa, norm, metadata_file])
            except subprocess.CalledProcessError:
                print_message("\nError during MaAsLin2 bash launch\n")


def run_metadata(sh_metadata, metadata):
    try:
        subprocess.run(["bash", sh_metadata, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during metadata bash launch\n")


def run_normalization(
    sh_normalization, taxa_type, normalization_type, metadata, imputation
):
    try:
        if normalization_type == "all" and taxa_type == "all":
            for taxa in ["asv", "genus", "species"]:
                for norm in ["gmpr", "clr"]:
                    subprocess.run(
                        [
                            "bash",
                            sh_normalization,
                            taxa,
                            norm,
                            metadata,
                            imputation,
                        ]
                    )
        elif normalization_type == "all" and taxa_type != "all":
            for norm in ["gmpr", "clr"]:
                subprocess.run(
                    ["bash", sh_normalization, taxa_type, norm, metadata, imputation]
                )
        elif normalization_type != "all" and taxa_type == "all":
            for taxa in ["asv", "genus", "species"]:
                subprocess.run(
                    [
                        "bash",
                        sh_normalization,
                        taxa,
                        normalization_type,
                        metadata,
                        imputation,
                    ]
                )
        elif normalization_type != "all" and taxa_type != "all":
            subprocess.run(
                [
                    "bash",
                    sh_normalization,
                    taxa_type,
                    normalization_type,
                    metadata,
                    imputation,
                ]
            )
    except subprocess.CalledProcessError:
        print_message("\nError during normalization bash launch\n")


def run_metrics(sh_metrics, taxa_type, normalization_type, metadata):
    print_message("Starting metrics analysis...")
    taxa_mapping = {
        "asv": {
            "script": "phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/10.1_asv_",
        },
        "species": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/10.3_species_",
        },
        "genus": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/10.2_genus_",
        },
    }

    taxa_types = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
    normalization_types = (
        ["gmpr", "clr"] if normalization_type == "all" else [normalization_type]
    )
    print_message(
        f"Choose CAREFULLY the sampling depth for {taxa_types} and {normalization_types} data\n"
        + "Based on the data extracted from the sampling\n"
        + "I reccomand to use for:\n"
        + "asv --> (gmpr,clr) --> (min_frequency or more, median or more)\n"
        + "gmpr--> (gmpr,clr) --> (first quantile or more, median or more)\n"
        + "species--> (gmpr,clr) --> (first quantile or more, median or more)\n"
    )
    try:
        for taxa in taxa_types:
            for norm in normalization_types:
                print_message(f"Metrics for {taxa} {norm} data")
                quantile_row = quantile_choice()
                quantile = read_quantile(
                    f"{taxa_mapping[taxa]['data_path']}{norm}_table_norm/{taxa}_{norm}_summary.csv",
                    quantile_row,
                )[0]
                print(f"Quantile chosen: {quantile}")
                subprocess.run(
                    [
                        "bash",
                        f"{sh_metrics}{taxa_mapping[taxa]['script']}",
                        taxa,
                        norm,
                        metadata,
                        f"{quantile[0]}",
                    ]
                )
    except subprocess.CalledProcessError:
        print_message("\nError during metrics bash launch\n")


def run_barplot(sh_barplot, normalization_type, metadata):
    """
    Runs the barplot bash script.

    Args:
    sh_barplot (str): The path to the barplot bash script.
    normalization_type (str): The normalization type.
    metadata (str): The metadata file name.

    Returns:
    None
    """
    try:
        if normalization_type == "all":
            for norm in ["gmpr", "clr"]:
                subprocess.run(["bash", sh_barplot, norm, metadata])
        else:
            subprocess.run(["bash", sh_barplot, normalization_type, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during barplot bash launch\n")
