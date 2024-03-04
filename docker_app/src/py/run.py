import subprocess
import zipfile
import pandas as pd
from message import print_message, print_explanation
from choice import column_for_ancom_choice, quantile_choice
from utility import read_quantile
from plot_csv import plot_feature_table_3d_histogram, create_heatmap
import os
import glob
from rich_table_display import display_csv_summary_with_rich
from utility import export_all_usefull_informations, eliminate_feature_not_true, calculate_standard_deviation
from trasnsalte_features import translate_feature
from significative_ANCOM import full_significative_analysis
from intersecate_MaAsLin_ANCOM import intersecate_MaAsLin_ANCOM

def run_denoising(path_denosing_sh, metadata_file, quality_value):
    correct_input = False
    while not correct_input: 
        choice = input("Do you want to run the denoising? [y/n]")
        if choice == "y":
            try:
                subprocess.run(["bash", path_denosing_sh, str(quality_value), metadata_file])
                correct_input = True
            except subprocess.CalledProcessError:
                print_message("\nError during denoising bash launch\n")
        elif choice == "n":
            correct_input = True
        
        
def run_ANCOM(sh_ANCOM, taxa_type, normalization, metadata_file):
    path_metadata = f"/home/microbiome/data/0_piglets_metadata/{metadata_file}"
    metadata_df = pd.read_csv(path_metadata, sep="\t")
    col_name = column_for_ancom_choice(metadata_df)
    taxa_list = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
    normalizations = ["gmpr", "clr"] if normalization == "all" else [normalization]
    for norm in normalizations:
        for taxa in taxa_list:
            print_message(f"ANCOM for {taxa} {norm} data")
            taxa_value = {"asv": "1", "genus": "2", "species": "3"}
            display_csv_summary_with_rich(f"/home/microbiome/data/6.{taxa_value[taxa]}_{taxa}_{norm}_table_norm/summary.csv")
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
                export_all_usefull_informations(f"/home/microbiome/data/8.{taxa_value[taxa]}_{taxa}_{norm}_DA_ANCOM/", f"/home/microbiome/data/8.{taxa_value[taxa]}_{taxa}_{norm}_DA_ANCOM/")
                eliminate_feature_not_true(f"/home/microbiome/data/8.{taxa_value[taxa]}_{taxa}_{norm}_DA_ANCOM/ancom.tsv", f"/home/microbiome/data/8.{taxa_value[taxa]}_{taxa}_{norm}_DA_ANCOM/percent-abundances.tsv")
                if taxa == "asv":
                    translate_feature(f"/home/microbiome/data/taxonomy/taxonomy.tsv", f"/home/microbiome/data/8.1_asv_{norm}_DA_ANCOM/percent-abundances_filtered.csv")
                full_significative_analysis(f"/home/microbiome/data/8.{taxa_value[taxa]}_{taxa}_{norm}_DA_ANCOM/percent-abundances_filtered.csv")
            except subprocess.CalledProcessError:
                print_message("\nError during ANCOM bash launch\n")
                
    
    
def run_MASLIN(sh_MASLIN, taxa_type, normalization, metadata_file):
    """Run MaAsLin2 analysis."""
    path_to_data = '/home/microbiome/data/'
    subprocess.run(['bash', '-c', f'find {path_to_data} -name "9*" -exec rm -rf {{}} +'])
    taxa_types = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
    normalizations = ["gmpr", "clr"] if normalization == "all" else [normalization]
    for norm in normalizations:
        for taxa in taxa_types:
            try:
                subprocess.run(["bash", sh_MASLIN, taxa, norm, metadata_file])
                if taxa == "asv":
                    translate_feature(f"/home/microbiome/data/taxonomy/taxonomy.tsv", f"/home/microbiome/data/9.1_asv_{norm}_DA_MaAsLin2/significant_results.tsv", "feature", "\t")
            except subprocess.CalledProcessError:
                print_message("\nError during MaAsLin2 bash launch\n")


def run_metadata(sh_metadata, metadata):
    try:
        subprocess.run(["bash", sh_metadata, metadata])
    except subprocess.CalledProcessError:
        print_message("\nError during metadata bash launch\n")

def run_get_infromations():
    correct_input = False
    while not correct_input:
        choice = input("Whant to check if the data are compositional? [y/n]")
        if choice == "y":
            correct_input = True    
            imputation_dict = {"3.1": "feature_table_imp", "3.2": "feature_table_imp_nrm", "3.3": "feature_table_imp_lgn"}
            for key, value in imputation_dict.items():
                try:
                    export_all_usefull_informations(f"/home/microbiome/data/{key}_{value}/", f"/home/microbiome/data/{key}_{value}/")
                except FileNotFoundError:
                    print_message(f"Error during export of {value} data")
                    continue
                
            normalizations = ["gmpr", "clr"]
            taxa_dict = {"asv":"1", "genus":"2", "species":"3"}
            for taxa, value in taxa_dict.items():
                try:
                    export_all_usefull_informations(f"/home/microbiome/data/4.{value}_{taxa}_table/", f"/home/microbiome/data/4.{value}_{taxa}_table/")
                    export_all_usefull_informations(f"/home/microbiome/data/5.{value}_{taxa}_table_taxafilt/", f"/home/microbiome/data/5.{value}_{taxa}_table_taxafilt/")
                except FileNotFoundError:
                    print_message(f"Error during export of {taxa} data")
                    continue
            for taxa, value in taxa_dict.items():
                for norm in normalizations:
                    try:
                        export_all_usefull_informations(f"/home/microbiome/data/6.{value}_{taxa}_{norm}_table_norm/", f"/home/microbiome/data/6.{value}_{taxa}_{norm}_table_norm/")
                    except FileNotFoundError:
                        print_message(f"Error during export of {taxa} {norm} data")
                        continue
                    
            print_message("Those are the standard deviation for the different tables\n"+
                          "N.B: The standard deviation should be <= 25% to mantain the data compositional")
            for taxa, value in taxa_dict.items():
                std, sdt_perc = calculate_standard_deviation(f"/home/microbiome/data/5.{value}_{taxa}_table_taxafilt/sample-frequency-detail.csv")
                print(f"Standard deviation for {taxa} in table taxa filt: {std} and {sdt_perc}%")
                for norm in normalizations:
                    std, std_perc = calculate_standard_deviation(f"/home/microbiome/data/6.{value}_{taxa}_{norm}_table_norm/sample-frequency-detail.csv")
                    print(f"Standard deviation for {taxa} in table norm {norm}: {std} and {std_perc}%")
        elif choice == "n":
            correct_input = True
                
def run_normalization(
    sh_normalization, taxa_type, normalization_type, metadata, imputation
):
    
    taxa_mapping = {
        "asv": {
            "script": "phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/6.1_asv_",
            "number": "1"
        },
        "species": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/6.3_species_",
            "number": "3"
        },
        "genus": {
            "script": "non-phylogenetic-core-analysis.sh",
            "data_path": "/home/microbiome/data/6.2_genus_",
            "number": "2"
        },
    }
    correct_input = False
    while not correct_input:
        choice = input("Do you want to run the normalization step? [y/n]")
        if choice == "y":
            taxa_types = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type] 
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
        elif choice == "n":
            correct_input = True
        
    correct_input = False
    while not correct_input:
        choice = input("whant to export all the usefull informations? [y/n]")
        if choice == "y":
            correct_input = True
            for taxa in taxa_mapping.keys():
                try:
                    export_all_usefull_informations(f"/home/microbiome/data/5.{taxa_mapping[taxa]['number']}_{taxa}_table_taxafilt/", f"/home/microbiome/data/5.{taxa_mapping[taxa]['number']}_{taxa}_table_taxafilt/")
                except Exception as e:
                    print_message(f"Error during export of {taxa} data: {str(e)}")
                    continue
        elif choice == "n":
            correct_input = True

def run_metrics(sh_metrics, taxa_type, normalization_type, metadata):
    corrct_input = False
    while not corrct_input:
        choice = input("Do you want to run the metrics analysis? [y/n]")
        corrct_input = True
        if choice == "y":
            print_message("-->Starting metrics analysis:")
            taxa_mapping = {
                "asv": {
                    "script": "phylogenetic-core-analysis.sh",
                    "data_path": "/home/microbiome/data/6.1_asv_",
                    "number": "1"
                },
                "species": {
                    "script": "non-phylogenetic-core-analysis.sh",
                    "data_path": "/home/microbiome/data/6.3_species_",
                    "number": "2"
                },
                "genus": {
                    "script": "non-phylogenetic-core-analysis.sh",
                    "data_path": "/home/microbiome/data/6.2_genus_",
                    "number": "3"
                },
            }

            taxa_types = ["asv", "genus", "species"] if taxa_type == "all" else [taxa_type]
            normalization_types = (
                ["gmpr", "clr"] if normalization_type == "all" else [normalization_type]
            )
            try:
                for taxa in taxa_types:
                    for norm in normalization_types:
                        print_message(f"--> Metrics for: {taxa} {norm} ")
                        display_csv_summary_with_rich(f"{taxa_mapping[taxa]['data_path']}{norm}_table_norm/summary.csv")
                        quantile_row = quantile_choice()
                        quantile = read_quantile(
                            f"{taxa_mapping[taxa]['data_path']}{norm}_table_norm/summary.csv",
                            quantile_row,
                        )[0]
                        print(f"--> Quantile chosen: {quantile}")
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
        elif choice == "n":
            corrct_input = True    

def run_intersecate_ANCOM_MaAsLin():
    start = True
    print_explanation(f"This script will run the intersecate ANCOM MaAsLin\n",
                      "N.B: Cause proble if both ANCOM and MaAsLin are not runned\n")
    while start:
        choice = input("Do you want to run the intersecate ANCOM MaAsLin? [y/n]")
        if choice != 'y' or choice !='n':
            start = False 
    if choice == "y":
        base_data_path = "/home/microbiome/data/"
        dict_taxa_path = {  'asv':{'number': '1',
                                 'path_ancom': '8.1_asv_gmpr_DA_ANCOM',
                                 'path_maslin': '9.1_asv_gmpr_DA_MaAsLin2', 
                                 'path_output': '10.1_asv_results/intersecate_MaAsLin_ANCOM.csv'},
                            'genus':{'number': '2',
                                     'path_ancom': '8.2_genus_gmpr_DA_ANCOM',
                                     'path_maslin': '9.2_genus_gmpr_DA_MaAsLin2',
                                     'path_output': '10.2_genus_results/intersecate_MaAsLin_ANCOM.csv'},
                            'species':{'number': '3',
                                       'path_ancom': '8.3_species_gmpr_DA_ANCOM',
                                       'path_maslin': '9.3_species_gmpr_DA_MaAsLin2',
                                       'path_output': '10.3_species_results/intersecate_MaAsLin_ANCOM.csv'}} 
        try:
            for taxa, path in dict_taxa_path.items():
                intersecate_MaAsLin_ANCOM(f"{base_data_path}{path['path_ancom']}/percent-abundances_filtered.csv", f"{base_data_path}{path['path_maslin']}/significant_results.tsv", f"{base_data_path}{path['path_output']}")
        except subprocess.CalledProcessError:
            print_message(f"\nError during intersecate ANCOM MaAsLin for {taxa}\n")
    else:
        print_message("Intersecate ANCOM MaAsLin not run")   
    
def run_imputation(sh_imputation, metadata_file):
    correct_input = False
    while not correct_input:
        choice = input("Do you wan tot perform the imputation step? [y/n]")
        if choice == "y":
            dir_tree = {"r": "rooted", "u": "unrooted", "n": "no_tree"}
            correct_input = False
            while not correct_input:
                choice = input("Do you want to use as distance matrix for mImpute [rooted or urooted or notree]? [r/u/n]")
                if choice == "r" or choice == "u":
                    print(f"Running imputation with {dir_tree[choice]} tree")
                    subprocess.run(["bash", sh_imputation, metadata_file, "y" ,dir_tree[choice]])
                    correct_input = True
                elif choice == "n":
                    subprocess.run(["bash", sh_imputation, metadata_file, "n", dir_tree[choice]])
                    correct_input = True
                else:
                    print_message("Incorrect Input")
            correct_input = False
            while not correct_input:
                choice = input("Do you want create plot for the different count of sequences? [y/n]")
                path_data = "/home/microbiome/data/"
                if choice == "y":
                    correct_input = True
                    path_row = f"{path_data}3_feature_tables/feature_table.csv"
                    path_imputed = f"{path_data}3.1_feature_table_imp/feature_table_imp.csv"
                    path_imputed_nrm = f"{path_data}3.2_feature_table_imp_nrm/feature_table_imp_nrm.csv"
                    path_imputed_lgn = f"{path_data}3.3_feature_table_imp_lgn/feature_table_imp_lgn.csv"
                    for path in [path_row, path_imputed, path_imputed_nrm, path_imputed_lgn]:
                        if os.path.exists(path):
                            print(f"Creating 3D histogram for {path}")
                            df = pd.read_csv(path)
                            plot_feature_table_3d_histogram(df, os.path.join('/'.join(path.split('/')[:-1]), f'3D_histogram_{os.path.basename(path).split(".")[0]}.png'))
                            if path != path_row:
                                print(f"Creating heatmap for {path}")
                                create_heatmap(path_row, path, os.path.join('/'.join(path.split('/')[:-1]), f'heatmap_{os.path.basename(path).split(".")[0]}.png'))
                elif choice == "n":
                    correct_input = True
        elif choice == "n":
            correct_input = True