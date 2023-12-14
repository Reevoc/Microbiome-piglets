# %% [markdown]
# ## Libraries
# %% Import LIbaries
import pandas as pd
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# %% [markdown]
# ## TODO:
# - [x] Time is categorical is better if it is numerical
# Spit in 3 different metadata files for different time: DONE
# - [x] check for wunded: DONE
# ## Metadata
# %%
path_name = "/home/piermarco/Documents/Thesis/data/0.2_piglets_metadata/"
# path_name = "/home/microbiome/data/0.2_piglets_metadata/"
metadta_file = os.path.join(path_name, "piglets_metadata.tsv")
metadata = pd.read_csv(metadta_file, sep="\t")
metadata = pd.DataFrame(metadata)
print(metadata.head())


def save_metadata(metadata, metadata_file_name):
    """
    Saves the metadata dataframe to a file.

    Args:
    metadata (pandas.DataFrame): The metadata dataframe.
    meradata_file_name (str): The name of the metadata file.

    Returns:
    None
    """
    new_path_name = path_name
    if not os.path.exists(new_path_name):
        os.makedirs(new_path_name)
    metadata.to_csv(
        os.path.join(new_path_name, metadata_file_name), sep="\t", index=False
    )


def generate_correlation_matrix(metadata):
    """
    Generates and plots the correlation matrix for the numeric columns in the metadata.

    Args:
    metadata (pandas.DataFrame): The metadata dataframe.

    Returns:
    None
    """
    is_numeric = metadata.iloc[0] == "numeric"
    numeric_columns = metadata.columns[is_numeric]
    numeric_data = metadata[numeric_columns].iloc[1:]
    numeric_data = numeric_data.apply(pd.to_numeric, errors="coerce")

    corr_matrix = numeric_data.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()


def perform_pca(metadata):
    """
    Performs Principal Component Analysis (PCA) on the numeric columns of the metadata.

    Args:
    metadata (pandas.DataFrame): The metadata dataframe.

    Returns:
    None
    """
    is_numeric = metadata.iloc[0] == "numeric"
    numeric_columns = metadata.columns[is_numeric]
    numeric_data = metadata[numeric_columns].iloc[1:]
    numeric_data = numeric_data.apply(pd.to_numeric, errors="coerce")

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data.select_dtypes(include=[np.number]))

    pca = PCA(n_components=2)  # You can change the number of components
    pca_result = pca.fit_transform(scaled_data)

    plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Dataset")
    plt.show()

    print("Variance explained by each component:", pca.explained_variance_ratio_)


generate_correlation_matrix(metadata)
perform_pca(metadata)


# %% [markdown]
# ### Modification of ANIMAL_ID
#
# Add the time column [time][numerical]{0, 1, 2} --> correspoding to the time in [Animal ID]{T0, T1, T2}
#
# Add the sow column [sow][numerical]{1, 2, 3, ..., 10} --> correspoding to the sow in [Animal ID]{S0, S1, S2, ..., S10}
#
# Add the sow_son column [sow_son][numerical]{10, 11, 12, ..., 100} --> correspoding to the sow in [Animal ID]{S1_P0, S1_P1, S2_P2, ..., S10_P0}
#
#
# %%
metadata_animalID_sow = metadata[["Animal ID", "sow"]]
metadata_time = metadata_animalID_sow["Animal ID"].copy()
metadata_sow_mother_son = metadata["Animal ID"].copy()
metadata_sow_mother = metadata["Animal ID"].copy()

metadata_sow_mother_son[0] = "numeric"
metadata_sow_mother[0] = "numeric"
metadata_time[0] = "numeric"

for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    int(sow_mother)
    metadata_sow_mother.replace(sow, sow_mother, inplace=True)

for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    sow_son = sow_mother + (sow.split("_")[1])[1]
    int(sow_son)
    metadata_sow_mother_son.replace(sow, sow_son, inplace=True)

metadata_time[1:] = metadata_animalID_sow["Animal ID"][1:].str[-1:]

metadata["time"] = metadata_time
metadata["sow_child"] = metadata_sow_mother_son
metadata["sow"] = metadata_sow_mother

metadata.drop("Animal ID", axis=1, inplace=True)
metadata.drop("sow", axis=1, inplace=True)
# %% [markdown]
#
# ### Percentage
# Why am I conducting this study?
#
# E.g.:
#
# I aim to investigate whether there is a correlation between
# the number of piglets in the nest and the number of piglets alive.
# The values provided in the table are merely numerical, making comparisons challenging.
# This challenge arises from the variation in nest sizes; one nest can be larger while another smaller.
# For instance, a nest with 10 piglets and 3 deaths is not equivalent to a nest with 20 piglets and 3 deaths.
#
# To address this issue, I have chosen to eliminate certain columns and replace them with categorical ones,
# utilizing percentage and mean calculations.

# %% [markdown]
# #### Study on Death and Alive Piglets

# I created a proportion: $\frac{nest_{piglets}}{100} = \frac{dead_{piglets}}{dead_{percentage}}$. Then, I divided the piglets into two groups: *high-survivability* and *low-survivability*.

# %%
metadata_nest_dead = metadata[["nest", "dead"]]
perc_dead = metadata_nest_dead[1:].apply(
    lambda x: int(x["dead"]) * 100 / int(x["nest"]), axis=1
)
mean_dead = perc_dead.mean()
metadata_dead = metadata["swab_ID"].copy()
for i in range(1, len(metadata_dead)):
    if perc_dead[i] < mean_dead:
        metadata_dead[i] = "high-survivability"
    else:
        metadata_dead[i] = "low-survivability"
metadata["survivability"] = metadata_dead


# %% [markdown]
# #### Study on the Number of Piglets in the Nest

# I calculated the mean of the number of piglets in the nest and categorized the piglets into two groups: *big-nest* and *small-nest*.

# %%
metadata_nest_convert_int = metadata["nest"][1:].apply(lambda x: int(x))
metadata_nest_mean = metadata_nest_convert_int.mean()
metadata_nest = metadata["swab_ID"].copy()
for i in range(1, len(metadata_nest)):
    if metadata_nest_convert_int[i] < metadata_nest_mean:
        metadata_nest[i] = "small-nest"
    else:
        metadata_nest[i] = "big-nest"
metadata["nest_size"] = metadata_nest


# %% [markdown]
#
# #### Study on the Number of Piglets Eliminated Due to Underweight
#
# I created a proportion: $ \frac{nest}{100} = \frac{underweight}{underweight_{perc}}$. Then, I divided the piglets into two groups: underweight and not underweight. In this case, I only considered piglets after time $T_0$.

# %%
metadata_nest_underweight = metadata[["nest", "uw_el"]]

perc_dead = metadata_nest_underweight[1:].apply(
    lambda x: (int(x["uw_el"]) * 100 / (int(x["nest"]))), axis=1
)
mean_dead = perc_dead.mean()
metadata_dead = metadata["swab_ID"].copy()

for i in range(1, len(metadata_dead)):
    if perc_dead[i] < mean_dead:
        metadata_dead[i] = "UW_nest_size"
    else:
        metadata_dead[i] = "not_UW_nest_size"
metadata["UW_nest_size"] = metadata_dead

# %% [markdown]
# #### Study on the number of piglets transferred
#
# Just bring to 0 the transferred piglets aftere time T0
# %%
metadata_transferred = metadata["transferred"].copy()
metadata_transferred_time = metadata[["time", "transferred"]]
metadata_transferred[1:] = metadata_transferred_time[1:].apply(
    lambda x: 0 if x["time"] != "0" else x["transferred"], axis=1
)
metadata["transferred_time"] = metadata_transferred
save_metadata(metadata, "piglets_metadata_new.tsv")

# %% [markdown]
# ### ARISING PROBLEM (Inconsistent Data?)
#
# There are five columns strictly correlated with the number of piglets:
#
# 1. **nest:** Number of piglets in the nest.
#
# 2. **alive:** Number of piglets alive.
#
# 3. **dead:** Number of piglets dead.
#
# 4. **uw_el:** Number of piglets underweight.
#
# 5. **transferred:** Number of piglets transferred T0.

# %% [markdown]
# #### Study over the time
# -[x] We don't know when piglets die
#
# -[x] We don't know when piglets are transferred based on metadata provided we suppoese time t0
#
# -[x] We don't know when piglets are underweight
#
# -[x] We know at the end how many pigles are alive but not at the correct time
#
# Based on some check the coorect formula seems to be the following one:
# $$ {alive}_{T0} = {nest}_{T0} - {dead}_{T0} $$
# $$ {weaned}_{T2} = {alive}_{T0} - {transferred}_{T1T2} - {underweight}_{T1T2} $$
# %%
# Convert columns to numeric
columns_to_convert = ["nest", "alive", "weaned", "dead", "transferred", "uw_el"]
metadata_new = metadata.copy()
metadata_new = metadata_new[1:]
for col in columns_to_convert:
    metadata_new[col] = pd.to_numeric(metadata[col], errors="coerce")
check_alive = metadata_new["alive"] == metadata_new["nest"] - metadata_new["dead"]
check_weaned = (
    metadata_new["weaned"]
    == metadata_new["alive"] - metadata_new["transferred"] - metadata_new["uw_el"]
)

for check in check_alive:
    if check != True:
        print("miss equation in check_alive")

for check in check_weaned:
    if check != True:
        print("miss equation in check_weaned")

# %% [markdown]
# ### Drop and rename column and save the new metadata file
# %%
metadata.drop("swab_ID", axis=1, inplace=True)
metadata.rename(columns={"neigh": "cell"}, inplace=True)
