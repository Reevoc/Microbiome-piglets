import pandas as pd
import numpy as np
import os

def ancom_log_ratio(file_path):
    data = pd.read_csv(file_path, sep=',')
    groups = list(set(data.iloc[0, 1:].values))
    percentiles = sorted(set(value.split('.')[0] for value in data.columns if value != 'Percentile'), key=lambda x: float(x))
    data = data.iloc[1:]
    data.columns = ['Perc_group'] + [f"{group}_{percentile}" for group in groups for percentile in percentiles]
    print(data.head())
    for group in groups:
        weighted_columns = []
        for percentile in percentiles:
            weighted_columns.append(f"{group}_{percentile}")
        for i in range(1, len(data) + 1):   
            weighted_mean = np.average(data.loc[i,weighted_columns].astype(float), weights= [1,1,1,1,1])
            data.loc[i, f"{group}_weighted"] = weighted_mean
    
    name_cols_weighted = [f"{group}_weighted" for group in groups]

    for i in range(1, len(data) + 1):
        for j in range(1, len(name_cols_weighted)):
            data.loc[i, f'log_ratio({name_cols_weighted[0]}/{name_cols_weighted[j]})'] = np.log2(data.loc[i, name_cols_weighted[0]] / data.loc[i, name_cols_weighted[j]])
    return data, groups

def plot_heat_map_log_ratio(data, groups, data_path):
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Preparing the data for the heatmap
    log_ratio_columns = [f'log_ratio({groups[0]}_weighted/{group}_weighted)' for group in groups[1:]]
    
    if len(log_ratio_columns) >= 2:
        heatmap_data = data[log_ratio_columns]
        heatmap_data = heatmap_data.dropna()
        name_feature = [';'.join(row.split(';')[4:]) for row in data['Perc_group']]
        heatmap_data.index = name_feature
        plt.figure(figsize=(30, 10))  # Adjust size as needed
        ax = sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)  # Rotate y-axis labels to horizontal
        plt.xlabel("Log Ratio Groups")
        plt.ylabel("Features")
        plt.title("Heatmap of Log Ratios")
        plt.savefig(os.path.join(data_path, "heatmap_log_ratio.png")) 
    else:
        print("No heatmap generated, not enough groups")  
    
def full_significative_analysis(path_to_csv):
    result_data, group = ancom_log_ratio(path_to_csv)
    path_dir = list(path_to_csv.split("/")[:-1])
    result_data.to_csv("/".join(path_dir) + "/sigificative-log-ratio.csv", sep=',', index=False)
    plot_heat_map_log_ratio(result_data, group, "/".join(path_dir))
    
# def main():
#     full_significative_analysis("/home/piermarco/Documents/github/microbiome_piglets/data/8.1_asv_gmpr_DA_ANCOM/percent-abundances_filtered.csv")
#  
# if __name__ == "__main__":
#     main()   
