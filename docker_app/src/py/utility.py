import subprocess
import csv
import glob
import os
import pandas as pd
from message import print_message, print_explanation
import zipfile

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
    extract_qzv_files(base_path)
    directory_created = find_latest_directory(base_path)
    if directory_created is not None:
        export_pngs(os.path.join(base_path, directory_created, "data"), output_path) 
        export_csv(os.path.join(base_path, directory_created, "data"), output_path)
        export_tsv(os.path.join(base_path, directory_created, "data"), output_path)
        eliminate_subfolder(base_path)
    else:
        print_message("No directory created")
        return False
    
def export_specified_all_nwk(base_path, output_path):
    extract_qza_files(base_path)
    dirs = find_all_directory(base_path)
    list_nwk = ["_","rooted","unrooted","_"]
    for directory, nwk in zip(dirs, list_nwk):
        last_name = output_path.split("/")[-1].split(".")[0]
        last_name_modified = last_name + "_" + nwk
        output_path_new = output_path.split("/")[:-1]
        output_path_new = "/".join(output_path_new)
        try:
            export_nwk(os.path.join(base_path, directory, "data"), os.path.join(output_path_new, last_name_modified + ".nwk"))
        except:
            print_message("No nwk file found")
            continue
    eliminate_subfolder(base_path)
    
def eliminate_feature_not_true(path_csv_ancom, path_perc_abbundances):
    ancom_test_W = pd.read_csv(path_csv_ancom, sep='\t')
    perc_abb = pd.read_csv(path_perc_abbundances, sep='\t')

    significant_features = ancom_test_W[ancom_test_W['Reject null hypothesis'] == True]['Unnamed: 0'].tolist()
    
    filtered_perc_abb = perc_abb[perc_abb['Percentile'].isin(significant_features)]
    output_path = path_perc_abbundances.replace('.tsv', '_filtered.csv')
    filtered_perc_abb.to_csv(output_path, index=True)

    return filtered_perc_abb

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


            