import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import glob
import subprocess
import numpy as np

def find_tsv_quality_control(tsv_path):
    tsv = pd.read_csv(tsv_path, sep='\t')
    return tsv

def plot_quality_control(tsv, name):
    median_quality_scores = tsv.loc[tsv['Unnamed: 0'] == '50%'].drop('Unnamed: 0', axis=1).squeeze()
    second_quality_scores = tsv.loc[tsv['Unnamed: 0'] == '2%'].drop('Unnamed: 0', axis=1).squeeze()
    nineth_quality_scores = tsv.loc[tsv['Unnamed: 0'] == '9%'].drop('Unnamed: 0', axis=1).squeeze()
    twentyfifth_quality_scores = tsv.loc[tsv['Unnamed: 0'] == '25%'].drop('Unnamed: 0', axis=1).squeeze()
    twenty = np.full(301, 20)
    fiftheen = np.full(301, 15)
    twentyfive = np.full(301, 25)
    plt.figure(figsize=(12, 6))
    plt.plot(second_quality_scores, label='2% Percentile', color='red')
    plt.plot(nineth_quality_scores, label='9% Percentile', color='green')
    plt.plot(twentyfifth_quality_scores, label='25% Percentile', color='orange')
    plt.plot(median_quality_scores, label='50% Median', color='blue')
    plt.plot(twenty, label='Threshold', color='black', linestyle='--')
    plt.plot(fiftheen, label='Threshold', color='black', linestyle='--')
    plt.plot(twentyfive, label='Threshold', color='black', linestyle='--')
    plt.title('Quality Plot of Sequencing Reads - ' + name)
    plt.xlabel('Position in Read')
    plt.ylabel('Median Quality Score')
    plt.legend(loc='lower left')
    plt.savefig(f'/home/microbiome/data/2_paired-end-demux-trimmed/{name}_quality_plot.png')

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

def create_quality_threshold(tsv, percentile, quality_threshold, file, csv_file_path, overwrite=False):
    # Calculate the median values below the quality threshold
    median_values = tsv.loc[tsv['Unnamed: 0'] == f'{percentile}'].drop('Unnamed: 0', axis=1).squeeze()
    median_values = np.asarray(median_values)
    median_values_below_threshold = median_values[:] < quality_threshold
    sum_below_threshold = np.count_nonzero(median_values_below_threshold)

    # Determine forward or reverse from the file name
    for_or_back = file.split('-')[0]

    # Read the other CSV file to get the value from the specified position
    other_csv_data = pd.read_csv(csv_file_path)
    row_index = len(other_csv_data) - sum_below_threshold
    if for_or_back == 'forward':
        value_from_other_csv = other_csv_data.iloc[row_index, 1] 
    elif for_or_back == 'reverse':
        value_from_other_csv = other_csv_data.iloc[row_index, 2]

    output_file = f'/home/microbiome/data/2_paired-end-demux-trimmed/quality_threshold_{percentile}_{quality_threshold}.csv'
    with open(output_file, 'a' if not overwrite else 'w') as f:
        if overwrite:
            f.write('File, Count Below Threshold, Value From Other CSV\n')
        f.write(f'{file}, {sum_below_threshold}, {value_from_other_csv}\n')

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print('Error: 2 arguments are expected')
        sys.exit(1)

    if args[0] == '-q':
        try:
            quality_value = int(args[1])
        except ValueError:
            print('Error: Quality value must be an integer')
            sys.exit(1)

    base_path = '/home/microbiome/data/1_paired-end-demux/'
    
    extract_qzv_files(base_path)

    latest_dir = find_latest_directory(base_path)
    
    if latest_dir:
        overwrite = True
        data_path = os.path.join(base_path, latest_dir, 'data')
        for file in os.listdir(data_path):
            if file.endswith('summaries.tsv'):
                tsv_path = os.path.join(data_path, file)
                tsv = find_tsv_quality_control(tsv_path)
                plot_quality_control(tsv, os.path.splitext(file)[0])
                create_quality_threshold(tsv, '50%', quality_value, os.path.splitext(file)[0], overwrite)
                overwrite = False  # Set to False after the first iteration
        subprocess.run(["rm", "-rf", os.path.join(base_path, latest_dir)])
    else:
        print('Error: Could not find the latest directory')

if __name__ == '__main__':
    main()
