import os
import subprocess
from message import print_message, print_explanation
from rich_table_display import display_csv_summary_with_rich
from utility import extract_qzv_files, find_latest_directory, export_specified_all_nwk

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

def taxonomy_calassification_choice():
    print_explanation("Decide if you want to perform the taxonomy classification or not\n"+
                      "N.B. You need to performed the taxonomy classification  to create the trees")
    choice = input("Do you want to perform the taxonomy classification? [y/n]")
    if choice == "y":
        subprocess.run(["bash", "/home/microbiome/docker_app/src/sh/5-taxonomy_classification.sh"])

def tree_creation_choice():
    print_explanation("Decide if you want to create the tree or not\n"+
                      "N.B. You need to perfromr the tree creation once afters is saved in the data folder")
    choice = input("Do you want to create the tree? [y/n]")
    if choice == "y":
        subprocess.run(["bash", "/home/microbiome/docker_app/src/sh/phylogenetic_tree.sh"])
        export_specified_all_nwk("/home/microbiome/data/tree", "/home/microbiome/data/tree/tree.nwk")
        
def ANCOM_choice():
    correct_input = False
    while not correct_input:
        choice = input("Do you want to run ANCOM in qiime2? [y/n]")
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


def column_for_ancom_choice(metadata_df):
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


def quantile_choice():
    dict_quantile = {
        "1": "min",
        "2": "first",
        "3": "median",
        "4": "third",
        "5": "max",
        "6": "mean",
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


def MASLIN_choice():
    correct_input = False
    print_message(
        "If you want to modify random and fixed effect you can directly change the 10-diff_abb_MaAsLin2.sh file"
    )
    while not correct_input:
        print_explanation("Do you want to run MaAsLin2 in qiime2? [y/n]")
        choice = input("Enter your choice: ")
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print_message("\nError: Invalid choice. Please enter a valid choice.\n")

def quality_value_choice():
    print_message("Decide the quality value choice to generate, fist of all we share\n" +
                  "some data")
    list = [15, 20, 25]
    path_quality_script = "/home/microbiome/docker_app/src/py/quality_control.py"
    
    for quality in list:
        subprocess.run(["python", path_quality_script, "-q", str(quality)])
        display_csv_summary_with_rich(f"/home/microbiome/data/2_paired-end-demux-trimmed/quality_threshold_50%_{quality}.csv")
    
    correct_input = False
    dict_quality = {"1": 15,
                    "2": 20,
                    "3": 25,}
    
    while not correct_input:
        print_explanation("which quality value do you want to use?\n"+
                            "1) 15\n"+
                            "2) 20\n"+
                            "3) 25\n")
        quality = input("Enter the choice:")
        try: 
            if quality not in dict_quality:
                raise ValueError
            else:
                quality_value = dict_quality[quality]
                quality_value = int(quality_value)
                return quality_value
        except ValueError:
            print_message("The value insert is incorrect retry")
            
def taxonomy_choice():
    print_message("Decide if export the taxonimy file as csv to see the code and the realtive taxon")
    choice = input("Do you want to export the taxonomy file as csv? [y/n]")
    correct_input = False
    while not correct_input:
        if choice == "y":
            extract_qzv_files("/home/microbiome/data/taxonomy")
            directory = find_latest_directory("/home/microbiome/data/taxonomy")
            try:
                final_directory = os.path.join("/home/microbiome/data/taxonomy", directory, "data")
            except TypeError:
                print_message("The directory is empty")
            except FileNotFoundError:
                print_message("The directory data is not found")

            for file in os.listdir(final_directory):
                if file == "metadata.tsv":
                    subprocess.run(["mv", os.path.join(final_directory, file), "/home/microbiome/data/taxonomy/taxonomy.tsv"])
                    subprocess.run(["rm", "-rf", os.path.join("/home/microbiome/data/taxonomy", directory)])
            correct_input = True
        elif choice == "n":
            correct_input = True
               
                    
        
            
        
        
        
        

    
         
        
                
    
    