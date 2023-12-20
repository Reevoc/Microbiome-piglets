import os
from colorama import Fore, Style
import subprocess
import pandas as pd


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
        print_explanation("Choose between the following available metadata:\n")
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


def ANCOM_choice():
    correct_input = False
    while not correct_input:
        print_explanation("Do you want to run ANCOM in qiime2? [y/n]")
        choice = input("Enter your choice: ")
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print_message("\nError: Invalid choice. Please enter a valid choice.\n")


def table_choice():
    options = {"1": "asv", "2": "genus", "3": "species", "4": "all"}
    correct_input = False
    while not correct_input:
        print_explanation(
            "Normalization can be done using 4 taxa types: \n 1) asv \n 2) genus \n 3) species \n 4) all\n"
        )
        choice = input("Enter the number for the taxa type: ")
        taxa_type = options.get(choice)
        if taxa_type:
            correct_input = True
        else:
            print_message("\nError: Invalid choice. Please enter a valid number.\n")
    return taxa_type


def normalization_choice():
    options = {"1": "gmpr", "2": "clr"}
    correct_input = False
    while not correct_input:
        print_explanation(
            "Normalization can be done using 2 metrics: \n 1) gmpr \n 2) clr\n"
        )
        choice = input("Enter the number for normalization type: ")
        normalization_type = options.get(choice)
        if normalization_type:
            correct_input = True
        else:
            print_message("\nError: Invalid choice. Please enter a valid number.\n")
    return normalization_type


def imputation_choice():
    options = {
        "1": "feature_table_imp",
        "2": "feature_table_imp_nrm",
        "3": "feature_table_imp_lgn",
    }
    correct_input = False
    while not correct_input:
        print_explanation(
            "Imputation can be done using 3 feature tables:\n 1) feature_table_imp \n 2) feature_table_imp_nrm \n 3) feature_table_imp_lgn\n"
        )
        choice = input("Enter the number for the imputation type: ")
        imputation_type = options.get(choice)
        if imputation_type:
            correct_input = True
        else:
            print_message("\nError: Invalid choice. Please enter a valid number.\n")
    return imputation_type


def save_analysis_performed_choice():
    """
    Asks the user if he wants to save the analysis performed.

    Args:
        None

    Returns:
        bool: True if the user wants to save the analysis performed, False otherwise.
    """
    correct_input = False
    while not correct_input:
        print_explanation("Do you want to save the analysis performed? [y/n]")
        choice = input("Enter your choice: ")
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print_message("\nError: Invalid choice. Please enter a valid choice.\n")


def run_ANCOM(sh_ANCOM, normalization, metadata_file):
    path_metadata = f"/home/microbiome/data/0.2_piglets_metadata/{metadata_file}"
    metadata_df = pd.read_csv(path_metadata, sep="\t")

    find = True
    while find:
        dict_columns_name = {i + 1: col for i, col in enumerate(metadata_df.columns)}
        print(dict_columns_name)
        print("\n")
        print_explanation("Select the column name for ANCOM analysis: ")
        col_number = input("Enter the number for the column name: ")
        try:
            col_number = int(col_number)
            if col_number not in dict_columns_name:
                raise ValueError
            col_name = dict_columns_name[col_number]
            find = False
        except ValueError:
            print_message(
                "\nError: column name not valid. Please enter a valid column name.\n"
            )

    find = True
    while find:
        dict_column_value = {
            i + 1: val for i, val in enumerate(metadata_df[col_name].unique())
        }
        print(dict_column_value)
        print("\n")
        print_explanation("Select the column value for ANCOM analysis: ")
        value_number = input("Enter the number for the column value: ")
        try:
            value_number = int(value_number)
            if value_number not in dict_column_value:
                raise ValueError
            col_value = dict_column_value[value_number]
            find = False
        except ValueError:
            print_message(
                "\nError: column value not valid. Please enter a valid column value.\n"
            )

    # Running the ANCOM bash script
    try:
        subprocess.run(
            ["bash", sh_ANCOM, col_name, col_value, normalization, metadata_file]
        )
    except subprocess.CalledProcessError:
        print_message("\nError during ANCOM bash launch\n")


def run_metadata(sh_metadata, metadata):
    try:
        subprocess.run(["bash", sh_metadata, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during metadata bash launch\n")


def run_normalization(
    sh_normalization, taxa_type, normalization_type, metadata, imputation
):
    try:
        if (taxa_type == "asv") or (taxa_type == "genus") or (taxa_type == "species"):
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
        else:
            # Run normalization for all taxa types if 'all' is selected
            for t in ["asv", "genus", "species"]:
                subprocess.run(
                    [
                        "bash",
                        sh_normalization,
                        t,
                        normalization_type,
                        metadata,
                        imputation,
                    ]
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
        # Selecting appropriate script and minimum frequency based on taxa type
        if taxa_type == "asv":
            sh_metrics_overwrite = sh_metrics + "phylogenetic-core-analysis.sh"
            min_freq_path = f"/home/microbiome/data/10.1_asv_{normalization_type}_table_norm/min_freq.txt"
        elif taxa_type == "species":
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq_path = f"/home/microbiome/data/10.3_species_{normalization_type}_table_norm/min_freq.txt"
        elif taxa_type == "genus":
            sh_metrics_overwrite = sh_metrics + "non-phylogenetic-core-analysis.sh"
            min_freq_path = f"/home/microbiome/data/10.2_genus_{normalization_type}_table_norm/min_freq.txt"
        elif taxa_type == "all":
            # Handle 'all' option by running for each taxa type
            for t in ["asv", "genus", "species"]:
                run_metrics(sh_metrics, t, normalization_type, metadata)
            return

        min_freq = read_min_freq_from_txt(min_freq_path)
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
        subprocess.run(["bash", sh_barplot, normalization_type, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during barplot bash launch\n")


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
                f"/home/microbiome/data/0.2_piglets_metadata/{metadata}",
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
