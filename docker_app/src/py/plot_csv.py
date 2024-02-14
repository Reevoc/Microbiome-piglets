import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_feature_table_3d_histogram(data, path_name):
    """
    Plots a 3D histogram representation of a feature table.

    :param data: Pandas DataFrame with the feature table.
    :param row_limit: Integer, number of rows to include in the plot (default 50).
    :param col_limit: Integer, number of columns to include in the plot (default 50).
    """
    X, Y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))

    fig = plt.figure(figsize=(20, 14))
    ax = fig.add_subplot(111, projection='3d')

    xpos, ypos = X.ravel(), Y.ravel()
    zpos = np.zeros_like(xpos)
    dx = dy = 0.5 * np.ones_like(zpos)
    dz = data.values.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

    ax.set_xlabel('Feature Index (Columns)')
    ax.set_ylabel('Sample Index (Rows)')
    ax.set_zlabel('Counts')

    ax.set_title('3D Histogram of Feature Table Subset')

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

    # Plotting the difference as a heatmap
    plt.figure(figsize=(20, 14))
    sns.heatmap(difference, cmap='coolwarm', annot=False)
    plt.title('Difference Heatmap')
    plt.show()
    plt.savefig(f"/home/microbiome/{path_name}")

