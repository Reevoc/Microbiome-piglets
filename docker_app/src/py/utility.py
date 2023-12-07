import os
from colorama import Fore, Style
import subprocess


def print_message(message, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{message}{Style.RESET_ALL}")


def print_explanation(message, color=Fore.YELLOW, style=Style.BRIGHT):
    print_message(message, color, style)


def create_metadata_files(metadata_py):
    try:
        subprocess.run(["python3", metadata_py])
    except subprocess.CalledProcessError:
        print_message("\n Error during metadata python launch \n")


def metadata_choice(metadata_folder):
    correct_input = False
    while not correct_input:
        print_explanation("Choose between the following avaiable metadata:\n")
        tuple_number_metadata = []
        count = 0
        for file in os.listdir(metadata_folder):
            if file.split(".")[-1] == "tsv":
                count += 1
                tuple_number_metadata.append((count, file))

        for tuple_number, file in tuple_number_metadata:
            print_explanation(f"{tuple_number}) {file}")
        print("\n")
        metadata_file = input("Enter metadata file (just select a number): ")

        try:
            if int(metadata_file) not in range(1, count + 1):
                raise ValueError
            correct_input = True
        except ValueError:
            print_message(
                "\nError: metadata file not valid. Please enter a valid metadata file.\n"
            )
    return tuple_number_metadata[int(metadata_file) - 1][1]


def table_choice():
    correct_input = False
    while not correct_input:
        print_explanation(
            "Normalization can be done using 3 taxa types: \n 1) asv --> normalize on asv \n 2) genus --> normalize on genus \n 3) species --> normalize on species\n 4) all --> normalize on all taxa\n "
        )
        taxa_type = input("Enter taxa type (asv, genus, species, all): ")
        try:
            if (
                (taxa_type != "asv")
                and (taxa_type != "genus")
                and (taxa_type != "species")
                and (taxa_type != "all")
            ):
                raise ValueError
            else:
                correct_input = True
        except ValueError:
            print_message(
                "\nError: taxa type not valid. Please enter a valid taxa type.\n"
            )
    return taxa_type


def run_metadata(sh_metadata, metadata):
    try:
        subprocess.run(["bash", sh_metadata, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during metadata bash launch\n")


def normalization_choice():
    print_explanation(
        "We recommend using 'gmpr' to ensure the script works correctly. CLR normalization may have issues with negative values.\n"
    )
    correct_input = False
    while not correct_input:
        print_explanation(
            "\n Normalization can be done using 2 metrics: \n 1) gmpr --> launch gmpr normalization \n 2) clr --> launch clr normalization \n"
        )
        normalization_type = input("Enter normalization type (gmpr, clr): ")

        try:
            if (normalization_type != "gmpr") and (normalization_type != "clr"):
                raise ValueError
            else:
                correct_input = True
        except ValueError:
            print_message(
                "\nError: normalization type not valid. Please enter a valid normalization type.\n"
            )
    return normalization_type


def run_normalization(sh_normalization, taxa_type, normalization_type, metadata):
    try:
        if (taxa_type == "asv") or (taxa_type == "genus") or (taxa_type == "species"):
            subprocess.run(
                ["bash", sh_normalization, taxa_type, normalization_type, metadata]
            )
        else:
            subprocess.run(
                ["bash", sh_normalization, "asv", normalization_type, metadata]
            )
            subprocess.run(
                ["bash", sh_normalization, "genus", normalization_type, metadata]
            )
            subprocess.run(
                ["bash", sh_normalization, "species", normalization_type, metadata]
            )
    except subprocess.CalledProcessError:
        print_message("\nError during normalization bash launch\n")


def read_min_freq_from_txt(path_to_txt):
    with open(path_to_txt, "r") as file:
        min_freq = file.read()
    return min_freq


def run_metrics(sh_metrics, taxa_type, normalization_type, metadata):
    sh_metrics_overwrite = ""
    try:
        if taxa_type == "asv":
            sh_metrics_overwrite = sh_metrics + "phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.1_asv_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    taxa_type,
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
        elif taxa_type == "species":
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.3_species_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    taxa_type,
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
        elif taxa_type == "genus":
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.2_genus_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    taxa_type,
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
        elif taxa_type == "all":
            sh_metrics_overwrite = sh_metrics + "phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.1_asv_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    "asv",
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.2_genus_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    "genus",
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq = read_min_freq_from_txt(
                f"/home/microbiome/data/10.3_species_{normalization_type}_table_norm/min_freq.txt"
            )
            subprocess.run(
                [
                    "bash",
                    sh_metrics_overwrite,
                    "species",
                    normalization_type,
                    metadata,
                    min_freq,
                ]
            )
    except subprocess.CalledProcessError:
        print_message("\nError during metrics bash launch\n")
