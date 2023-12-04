# %% [markdown]
# # Libraries
# %% Import LIbaries
import pandas as pd
import numpy as np
import subprocess
import os

# %% [markdown]
# # Metadata

# %%
# TODO: change the path to work on microbiome not in local
path_name = "/home/piermarco/Documents/Thesis/data/0.2_piglets_metadata/"

metadta_file = os.path.join(path_name, "piglets_metadata.tsv")

metadata = pd.read_csv(metadta_file, sep="\t")
metadata = pd.DataFrame(metadata)

# %% [markdown]
# ## 1) Modification metadata
#
# Add the time column [time][numerical]{0, 1, 2} --> correspoding to the time in [Animal ID] [categorical]{T0, T1, T2}
#
# Add the sow column [sow][numerical]{1, 2, 3, ..., 10} --> correspoding to the sow in [Animal ID] [categorical]{S0, S1, S2, ..., S10}
#
# Add the sow_son column [sow_son][numerical]{10, 11, 12, ..., 100} --> correspoding to the sow in [Animal ID] [categorical]{S1_P0, S1_P1, S2_P2, ..., S10_P0}

# %%
metadata_animalID_sow = metadata[["Animal ID", "sow"]]
metadata_time = metadata_animalID_sow["Animal ID"].copy()
metadata_time[0] = "numeric"
metadata_time[1:] = metadata_animalID_sow["Animal ID"][1:].str[-1]
metadata["time"] = metadata_time

metadata_sow_mother_son = metadata["Animal ID"].copy()
metadata_sow_mother = metadata["Animal ID"].copy()
metadata_sow_mother_son[0] = "numeric"
metadata_sow_mother[0] = "numeric"

for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    sow_son = sow_mother + (sow.split("_")[1])[1]
    int(sow_son)
    metadata_sow_mother_son.replace(sow, sow_son, inplace=True)

for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    int(sow_mother)
    metadata_sow_mother.replace(sow, sow_mother, inplace=True)

metadata["sow_son"] = metadata_sow_mother_son
metadata["sow"] = metadata_sow_mother
metadata.drop("Animal ID", axis=1, inplace=True)


# %% [markdown]
# ### Output Metadata metadata_piglets_modified1.tsv

# %%
new_path_name = path_name + "modified/"
if not os.path.exists(new_path_name):
    os.makedirs(new_path_name)
metadata.to_csv(
    os.path.join(new_path_name, "piglets_metadata_modified1.tsv"), sep="\t", index=False
)
# %%
