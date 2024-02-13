import subprocess
import csv
import glob
import os
from message import print_message, print_explanation


def create_metadata_files(metadata_py):
    try:
        subprocess.run(["python3", metadata_py])
    except subprocess.CalledProcessError:
        print_message("\n Error during metadata python launch \n")


def read_quantile(path_csv, row_number):
    """
    Reads a CSV file and returns the row with the specified number.

    Args:
        path_csv (str): The path to the CSV file.
        row_number (int): The row number to match.

    Returns:
        list: A list of the 2 elements (col_ 1 ,col_2) of the row with the specified number.
    """
    tuple_freq_samp = []
    row_number = int(row_number)
    with open(path_csv, "r") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == row_number:
                sample = int(float(str(row[1]).replace(",", "")))
                feature = int(float(str(row[2]).replace(",", "")))
                tuple_freq_samp.append((sample, feature))
    return tuple_freq_samp




def save_analysis_performed(metadata, normalization_type, taxa_type, imputation):
    """
    Saves the analysis performed to respective folders.

    Args:
        metadata (str): The metadata filename.
        normalization_type (str): The normalization type.
        taxa_type (str): The taxa type.
        imputation (str): The imputation type.

    Returns:
        None
    """
    try:
        os.mkdir("/home/microbiome/analysis_performed")
    except FileExistsError:
        pass
    except Exception as e:
        print_message(f"\nError during creation of analysis_performed folder: {e}\n")

    name_analysis = f"{metadata}_{normalization_type}_{taxa_type}_{imputation}"
    base_dir = f"/home/microbiome/analysis_performed/{name_analysis}"

    try:
        # Create necessary directories
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(f"{base_dir}/metadata", exist_ok=True)
        os.makedirs(f"{base_dir}/normalization", exist_ok=True)
        os.makedirs(f"{base_dir}/metrics", exist_ok=True)

        print_message("\nCopying files to analysis_performed folder...\n")
        subprocess.run(
            [
                "cp",
                f"/home/microbiome/data/0_piglets_metadata/{metadata}",
                f"{base_dir}/metadata/",
            ]
        )
        print_message("\nMetadata file copied\n")
        subprocess.run(
            [
                "cp",
                "-r",
                f"/home/microbiome/data/10.1_asv_{normalization_type}_table_norm/",
                f"{base_dir}/normalization/",
            ]
        )

        subprocess.run(
            [
                "cp",
                f"/home/microbiome/data/10.2_genus_{normalization_type}_table_norm/genus_{normalization_type}_table_norm.qzv",
                f"{base_dir}/normalization/",
            ]
        )
        subprocess.run(
            [
                "cp",
                f"/home/microbiome/data/10.3_species_{normalization_type}_table_norm/species_{normalization_type}_table_norm.qzv",
                f"{base_dir}/normalization/",
            ]
        )
        print_message("\nNormalization files copied\n")
        subprocess.run(
            [
                "cp",
                "-r",
                f"/home/microbiome/data/11.1_asv_{normalization_type}_core_metrics_phylogenetic/",
                f"{base_dir}/metrics/",
            ]
        )
        subprocess.run(
            [
                "cp",
                "-r",
                f"/home/microbiome/data/11.2_genus_{normalization_type}_core_metrics_non-phylogenetic/",
                f"{base_dir}/metrics/",
            ]
        )
        subprocess.run(
            [
                "cp",
                "-r",
                f"/home/microbiome/data/11.3_species_{normalization_type}_core_metrics_non-phylogenetic/",
                f"{base_dir}/metrics/",
            ]
        )
        print_message("\nMetrics files copied\n")

    except Exception as e:
        print_message(f"\nError during creation of folder or file copying: {e}\n")

def eliminate_folder(base_path):
    data_path = os.path.join(base_path)
    folders = glob.glob(data_path + "/*")
    for folder in folders:
        subprocess.run(["rm", "-rf", folder])
        