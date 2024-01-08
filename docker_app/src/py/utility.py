import os
from colorama import Fore, Style
import subprocess
import pandas as pd
import csv


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
    options = {"1": "gmpr", "2": "clr", "3": "all"}
    correct_input = False
    while not correct_input:
        print_message(
            "If we want to use ANCOM as analysis it is suggested to perform all normalization \n"
            + "gmpr will be used for Alpha and Beta Analysis\n"
            + "clr for ANCOM (Further detail for the choice on the paper)\n"
        )
        print_explanation(
            "Normalization can be done using 2 metrics: \n 1) gmpr \n 2) clr\n 3) all\n"
        )
        choice = input("Enter the number for the normalization type: ")
        normalization_type = options.get(choice)
        print(normalization_type)
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
        print_message(
            "If we choose to use clr (centered log-ratio transformation), it is recommended\n"
            + "to only use feature_table_imp. Using the other two can cause issues due to the\n"
            + "creation of negative values in the analysis. On the other hand, GMPR (geometric\n"
            + "mean of pairwise ratios) works well with all three types of imputation.\n"
        )

        print_explanation(
            "Imputation can be done using 3 feature tables:\n"
            + "1) feature_table_imp \n"
            + "2) feature_table_imp_nrm \n"
            + "3) feature_table_imp_lgn \n"
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


def choose_column_for_ancom(metadata_df):
    """Choose the column name for ANCOM analysis."""
    mask_categorical = metadata_df.iloc[0, :] == "categorical"
    metadata_df = metadata_df.loc[:, mask_categorical]
    dict_columns_name = {i + 1: col for i, col in enumerate(metadata_df.columns)}
    print(dict_columns_name)
    while True:
        print_explanation("Select the column name for ANCOM analysis: ")
        col_number = input("Enter the number for the column name: ")
        try:
            col_number = int(col_number)
            if col_number not in dict_columns_name:
                raise ValueError
            return dict_columns_name[col_number]
        except ValueError:
            print_message(
                "\nError: column name not valid. Please enter a valid column name.\n"
            )


def choose_quantile():
    dict_quantile = {
        "1": "min",
        "2": "first",
        "3": "median",
        "4": "third",
        "5": "max",
        6: "mean",
    }

    while True:
        print_explanation(
            "Select quantile to use as frequency for excluding samples or features:\n1) min frequency \n2) first quantile\n3) median\n4) third quantile\n5) max frequency\n"
        )
        input_quantile = input("Enter the number for the quantile: ")
        try:
            if input_quantile not in dict_quantile:
                raise ValueError
            return input_quantile
        except ValueError:
            print_message(
                "\nError: quantile not valid. Please enter a valid quantile.\n"
            )


def read_csv(path_csv, row_number):
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


def run_ANCOM(sh_ANCOM, normalization, metadata_file):
    """Run ANCOM analysis."""
    path_metadata = f"/home/microbiome/data/0.2_piglets_metadata/{metadata_file}"
    metadata_df = pd.read_csv(path_metadata, sep="\t")

    col_name = choose_column_for_ancom(metadata_df)
    quantile_num = choose_quantile()

    # Running the ANCOM bash script
    try:
        subprocess.run(
            ["bash", sh_ANCOM, col_name, normalization, metadata_file, quantile_num]
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
    print_message("Choosing the quantile for the metrics analysis...")
    quantile_num = choose_quantile()

    print_message("Starting metrics analysis...")
    taxa_mapping = {
        "asv": {"script": "phylogenetic-core-analysis.sh", "data_path": "10.1_asv_"},
        "species": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "10.3_species_",
        },
        "genus": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "10.2_genus_",
        },
    }

    normalization_types = (
        ["gmpr", "clr"] if normalization_type == "all" else [normalization_type]
    )

    try:
        if taxa_type == "all":
            for t in taxa_mapping:
                for norm_type in normalization_types:
                    run_metrics(sh_metrics, t, norm_type, metadata)
        else:
            for norm_type in normalization_types:
                script = sh_metrics + taxa_mapping[taxa_type]["script"]
                path = f"/home/microbiome/data/{taxa_mapping[taxa_type]['data_path']}{norm_type}_table_norm/{taxa_type}_{norm_type}_summary.csv"
                print(path)
                frequency_data = read_csv(path, quantile_num)
                frequency_data = frequency_data[0][0]

                subprocess.run(
                    ["bash", script, taxa_type, norm_type, metadata, frequency_data]
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
