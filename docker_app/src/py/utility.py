import subprocess
import csv
import glob
import os
import pandas as pd
from message import print_message, print_explanation
import zipfile
import re

def create_metadata_files(metadata_py):
    try:
        subprocess.run(["python3", metadata_py])
    except subprocess.CalledProcessError:
        print_message("\n Error during metadata python launch \n")

def read_quantile(path_csv, row_number):
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

def eliminate_subfolder(base_path):
    subfolders = [f.path for f in os.scandir(base_path) if f.is_dir()]
    for subfolder in subfolders:
        subprocess.run(["rm", "-r", subfolder])

def extract_qzv_files(base_path):
    qzv_files = glob.glob(os.path.join(base_path, '*.qzv'))
    for qzv_file in qzv_files:
        with zipfile.ZipFile(qzv_file, 'r') as zip_ref:
            zip_ref.extractall(base_path)

def extract_qza_files(base_path):
    qza_files = glob.glob(os.path.join(base_path, '*.qza'))
    for qza_file in qza_files:
        with zipfile.ZipFile(qza_file, 'r') as zip_ref:
            zip_ref.extractall(base_path)

def find_all_directory(base_path):
    if not os.path.exists(base_path):
        return None
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return dirs

def find_latest_directory(base_path):
    if not os.path.exists(base_path):
        return None
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    dirs.sort(reverse=True)
    return dirs[0] if dirs else None

def export_pngs(base_path, output_path):
    try:
        images = glob.glob(os.path.join(base_path, '*.png'))
        for image in images:
            subprocess.run(["mv", image, output_path])
    except:
        print_message("No png file found")

def export_csv(base_path, output_path):
    try:
        csv_files = glob.glob(os.path.join(base_path, '*.csv'))
        for csv_file in csv_files:
            subprocess.run(["mv", csv_file, output_path])
    except:
        print_message("No csv file found")
        
def export_biom(base_path, output_path):
    try:
        biom_files = glob.glob(os.path.join(base_path, '*.biom'))
        for biom_file in biom_files:
            subprocess.run(["mv", biom_file, output_path])
    except:
        print_message("No biom file found")

def export_tsv(base_path, output_path):
    try:
        tsv_files = glob.glob(os.path.join(base_path, '*.tsv'))
        for tsv_file in tsv_files:
            subprocess.run(["mv", tsv_file, output_path])
    except: 
        print_message("No tsv file found")
    
def export_nwk(base_path, output_path):
    nwk_files = glob.glob(os.path.join(base_path, '*.nwk'))
    for nwk_file in nwk_files:
        subprocess.run(["mv", nwk_file, output_path])
    
def export_all_usefull_informations(base_path, output_path):
    try:
        extract_qzv_files(base_path)
        directory_created = find_latest_directory(base_path)
        if directory_created is not None:
            export_pngs(os.path.join(base_path, directory_created, "data"), output_path) 
            export_csv(os.path.join(base_path, directory_created, "data"), output_path)
            export_tsv(os.path.join(base_path, directory_created, "data"), output_path)
            eliminate_subfolder(base_path)
        else:
            return False
    except FileNotFoundError as e:
        print_message(f"FileNotFoundError: {e}")
        return False
    except Exception as e:
        print_message(f"An error occurred: {e}")
        return False

    
def export_biom_information(base_path, output_path):
    extract_qza_files(base_path)
    directory_created = find_latest_directory(base_path)
    if directory_created is not None:
        export_biom(os.path.join(base_path, directory_created, "data"), output_path)
        eliminate_subfolder(base_path)
    else:
        print_message("No directory created")
        return False
    
def export_specified_all_nwk(base_path, output_path):
    extract_qza_files(base_path)
    dirs = find_all_directory(base_path)
    for directory in dirs:
        last_name = output_path.split("/")[-1].split(".")[0]
        tree_file_path = os.path.join(base_path, directory, "data", "tree.nwk")
        try:
            with open(tree_file_path, "r") as file:
                text = file.read()
            if text.startswith("(("):
                print("--> Find rooted tree")
                last_name_modified = last_name + "_" + "rooted"
            if text.startswith("((("):
                print("--> Find unrooted tree")
                last_name_modified = last_name + "_" + "unrooted"
            output_path_new = "/".join(output_path.split("/")[:-1])
            try:
                export_nwk(os.path.join(base_path, directory, "data"), os.path.join(output_path_new, last_name_modified + ".nwk"))
            except:
                print_message("Failed to export nwk file")
                continue

        except FileNotFoundError:
            print_message(f"Tree file not found in {tree_file_path}, skipping.")
            continue

    eliminate_subfolder(base_path)


    
def eliminate_feature_not_true(path_csv_ancom, path_perc_abbundances):
    ancom_test_W = pd.read_csv(path_csv_ancom, sep='\t')
    perc_abb = pd.read_csv(path_perc_abbundances, sep='\t')
    significant_features = ancom_test_W[ancom_test_W['Reject null hypothesis'] == True]['Unnamed: 0'].tolist()
    filtered_perc_abb = perc_abb[perc_abb['Percentile'].isin(significant_features)]
    output_path = path_perc_abbundances.replace('.tsv', '_filtered.csv')
    first_row = perc_abb.iloc[[0]]
    filtered_perc_abb = pd.concat([first_row, filtered_perc_abb], ignore_index=True)

    filtered_perc_abb.to_csv(output_path, index=False)  
    return filtered_perc_abb

def calculate_standard_deviation(path_csv):
    try:
        data = pd.read_csv(path_csv)
        std_dev = data.iloc[:, 1].std()
        mean = data.iloc[:, 1].mean()
        std_dev_percent = (std_dev / mean) * 100
        return std_dev, std_dev_percent
    except FileNotFoundError:
        print(f"File not found: {path_csv}")
        return None, None 
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None, None  

def dataframe_summary(df):
    """
    Prints comprehensive summary information about a pandas DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to summarize.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input is not a pandas DataFrame.")
    print("General Information:")
    df.info()
    print("\nDescriptive Statistics:")
    print(df.describe(include='all'))
    print("\nData Types:")
    print(df.dtypes)
    print("\nShape of DataFrame:", df.shape)
    print("\nColumn Names:")
    print(df.columns)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nNumber of Unique Values:")
    print(df.nunique())
    print("\nMemory Usage:")
    print(df.memory_usage())
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())

def natural_sort_key(s, _nsre=re.compile("([0-9]+)")):
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def find_qzv_files(base_path):
    qzv_files = {}
    for root, dirs, files in os.walk(base_path):
        dirs.sort(key=natural_sort_key)  # Sort directories numerically
        for file in files:
            if file.endswith(".qzv"):
                dir_key = root.replace(base_path, "").strip("/")
                if dir_key not in qzv_files:
                    qzv_files[dir_key] = []
                qzv_files[dir_key].append(file)
    return qzv_files


def print_tree(qzv_files):
    count = -1
    new_dict = {}
    for dir_key, files in sorted(
        qzv_files.items(), key=lambda x: natural_sort_key(x[0])
    ):
        print(f"|{Style.BRIGHT}{Fore.GREEN}{dir_key}/{Style.RESET_ALL}")
        print("|")
        for file in sorted(files, key=natural_sort_key):
            count += 1
            if isinstance(file, str):
                print(
                    f"|___________{Fore.LIGHTCYAN_EX}{count}_{Fore.LIGHTBLUE_EX}{file}{Style.RESET_ALL}"
                )
                new_dict[count] = []
                new_key = f"{dir_key}/{file}"
                new_dict[count].append(new_key)
    return new_dict


def extract_number(s):
    if "." in s:
        s = s.replace(".", "")
        return int(s)
    else:
        return int(s + "0")


def get_file_from_tree(current_dict, keys):
    for key in keys:
        current_dict = current_dict.get(key, {})
        if not isinstance(current_dict, dict):
            return current_dict
    return None
