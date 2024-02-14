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
    twenty = np.full(280, 20)
    fiftheen = np.full(280, 15)
    twentyfive = np.full(280, 25)
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
    tick_interval = 20 
    plt.xticks(np.arange(0, len(median_quality_scores) + 1, tick_interval))
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

def create_quality_threshold(tsv, percentile, quality_threshold, file, overwrite=False):
    median_values = tsv.loc[tsv['Unnamed: 0'] == f'{percentile}'].drop('Unnamed: 0', axis=1).squeeze()
    median_values = median_values.to_numpy()
    right_trim = len(median_values) - 1 
    left_trim = 0  
    for i in range(len(median_values)):
        if median_values[i] < quality_threshold:
            right_trim = i
            break
    for i in range(len(median_values)):
        if median_values[i] > quality_threshold:
            left_trim = i
            break
    output_file = f'/home/microbiome/data/2_paired-end-demux-trimmed/quality_threshold_{percentile}_{quality_threshold}.csv'
    with open(output_file, 'a' if not overwrite else 'w') as f:
        if overwrite:
            f.write(f'File quality threshold {quality_threshold}, Left Trim, Right Trim\n')
        f.write(f'{file}, {str(left_trim)}, {str(right_trim)}\n')

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

    base_path = '/home/microbiome/data/2_paired-end-demux-trimmed/'
    
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
                overwrite = False  
        subprocess.run(["rm", "-rf", os.path.join(base_path, latest_dir)])
    else:
        print('Error: Could not find the latest directory')

if __name__ == '__main__':
    main()
