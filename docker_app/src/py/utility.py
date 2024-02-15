import subprocess
import csv
import glob
import os
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

def find_latest_directory(base_path):
    if not os.path.exists(base_path):
        return None
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    dirs.sort(reverse=True)
    return dirs[0] if dirs else None

def export_pngs(base_path, output_path):
    images = glob.glob(os.path.join(base_path, '*.png'))
    for image in images:
        subprocess.run(["mv", image, output_path])

def export_csv(base_path, output_path):
    csv_files = glob.glob(os.path.join(base_path, '*.csv'))
    for csv_file in csv_files:
        subprocess.run(["mv", csv_file, output_path])
    
def export_all_usefull_informations(base_path, output_path):
    extract_qzv_files(base_path)
    directory_created = find_latest_directory(base_path)
    if directory_created is not None:
        export_pngs(os.path.join(base_path, directory_created, "data"), output_path) 
        export_csv(os.path.join(base_path, directory_created, "data"), output_path)
        eliminate_subfolder(base_path)
    else:
        print_message("No directory created")
        return False
        
    