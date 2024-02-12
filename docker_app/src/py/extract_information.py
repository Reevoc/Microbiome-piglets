from quality_control import extract_qzv_files, find_latest_directory
import glob
import os
import pandas as pd
import subprocess

def path_directory_of_qzv(base_path):
    extract_qzv_files(base_path)
    directory = find_latest_directory(base_path)
    return directory

def eliminate_folder(directory, base_path):
    if directory:
        data_path = os.path.join(base_path, directory, 'data')
        for file in os.listdir(data_path):
            if file.endswith('.csv'):
                subprocess.run(["rm", "-rf", os.path.join(base_path, directory)])
                return os.path.join(data_path, file)
    else:
        print("Error: Could not find the any dir in the path")
        return None



