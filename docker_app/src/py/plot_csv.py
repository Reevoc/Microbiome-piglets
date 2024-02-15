import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_feature_table_3d_histogram(data, path_name):
    """
    Plots a 3D histogram representation of a feature table, omitting bins with a value of 0.

    :param data: Pandas DataFrame with the feature table.
    :param path_name: String, the path to save the histogram image.
    """
    X, Y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))

    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111, projection='3d')

    xpos, ypos = X.ravel(), Y.ravel()
    zpos = np.zeros_like(xpos)
    dz = data.values.ravel()

    # Filter out positions where dz (height of the bin) is 0
    mask = dz != 0
    xpos, ypos, zpos, dz = xpos[mask], ypos[mask], zpos[mask], dz[mask]

    dx = dy = 0.5 * np.ones_like(zpos)

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

    ax.set_xlabel('Feature Index (Columns)')
    ax.set_ylabel('Sample Index (Rows)')
    ax.set_zlabel('Counts')

    ax.set_title('3D Histogram of Feature Table')

    plt.show()
    plt.savefig(f"/home/microbiome/{path_name}")


def create_heatmap(csv_file_path1, csv_file_path2, path_name):
    """
    Creates a heatmap showing the difference between two CSV matrices.

    :param csv_file_path1: String, path to the first CSV file.
    :param csv_file_path2: String, path to the second CSV file.
    :param title: String, title of the heatmap.
    """
    # Load data from CSV files
    df1 = pd.read_csv(csv_file_path1)
    df2 = pd.read_csv(csv_file_path2)

    # Calculate the difference
    difference = df1 - df2
    summation_neg, summation_pos, count_neg, count_pos = 0, 0, 0, 0
    for i in range(difference.shape[0]):
        for j in range(difference.shape[1]):
            if difference.iloc[i,j] > 0:
                summation_pos += difference.iloc[i,j]
                count_pos += 1
            elif difference.iloc[i,j] < 0:
                summation_neg += difference.iloc[i,j]
                count_neg += 1
    lower_bound = summation_neg/count_neg
    upper_bound = summation_pos/count_pos
    difference = difference.clip(lower_bound, upper_bound)
    # Plotting the difference as a heatmapx
    plt.figure(figsize=(20, 14))
    sns.heatmap(difference, cmap='coolwarm', annot=False)
    plt.title('Difference Heatmap')
    plt.show()
    plt.savefig(f"/home/microbiome/{path_name}")

