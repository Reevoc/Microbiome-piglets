import pandas as pd
from utility import dataframe_summary

def create_list_feature(taxonomy_file):
    """Create mapping for tsv file"""
    with open(taxonomy_file, 'r') as f:
        lines = f.readlines()
        key_name = {}
        for line in lines:
            line = line.strip().split('\t')
            key_name[line[0]] = line[1]
    return key_name

def translate_feature(taxonomy_file, percent_abundances_file, column_to_translate = 'Percentile', separator=','):
    key_name = create_list_feature(taxonomy_file)
    percent_abundances = pd.read_csv(percent_abundances_file, sep=separator)  # Adjust the delimiter if needed

    # dataframe_summary(percent_abundances)

    # Make sure 'Percentile' is a correct column name
    if column_to_translate in percent_abundances.columns:
        for key, value in key_name.items():
            for row in percent_abundances[column_to_translate]:
                if key in row:
                    print(f"key: {key}, value: {value}, row: {row}")
                    percent_abundances[column_to_translate] = percent_abundances[column_to_translate].replace(row, value)
    else:
        print("Column 'Percentile' not found in DataFrame")
    percent_abundances.to_csv(percent_abundances_file, index=False, sep = separator)