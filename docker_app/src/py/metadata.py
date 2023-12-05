# %% [markdown]
# ## Libraries
# %% Import LIbaries
import pandas as pd
import os

# %% [markdown]
# ## Metadata

# %%
# TODO: change the path to work on microbiome not in local
path_name = "/home/microbiome/data/0.2_piglets_metadata/"

metadta_file = os.path.join(path_name, "piglets_metadata.tsv")

metadata = pd.read_csv(metadta_file, sep="\t")
metadata = pd.DataFrame(metadata)


# %%
def save_metadata(metadata, metadata_file_name):
    new_path_name = path_name
    if not os.path.exists(new_path_name):
        os.makedirs(new_path_name)
    metadata.to_csv(
        os.path.join(new_path_name, metadata_file_name), sep="\t", index=False
    )


# %% [markdown]
# ### 1) Modification metadata
#
# Add the time column [time][numerical]{0, 1, 2} --> correspoding to the time in [Animal ID] [categorical]{T0, T1, T2}
#
# Add the sow column [sow][numerical]{1, 2, 3, ..., 10} --> correspoding to the sow in [Animal ID] [categorical]{S0, S1, S2, ..., S10}
#
# Add the sow_son column [sow_son][numerical]{10, 11, 12, ..., 100} --> correspoding to the sow in [Animal ID] [categorical]{S1_P0, S1_P1, S2_P2, ..., S10_P0}


# %%
metadata_animalID_sow = metadata[["Animal ID", "sow"]]

metadata_time = metadata_animalID_sow["Animal ID"].copy()
metadata_sow_mother_son = metadata["Animal ID"].copy()
metadata_sow_mother = metadata["Animal ID"].copy()

# %% [markdown]
# ### Change the type of the columns from categorical to numerical

# %%
metadata_sow_mother_son[0] = "numeric"
metadata_sow_mother[0] = "numeric"
metadata_time[0] = "categorical"
# %% [markdown]
# ### Modify the values of the columns
# %%
for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    int(sow_mother)
    metadata_sow_mother.replace(sow, sow_mother, inplace=True)

for sow in metadata_animalID_sow["Animal ID"][1:]:
    sow_mother = (sow.split("_")[0]).replace("S", "")
    sow_son = sow_mother + (sow.split("_")[1])[1]
    int(sow_son)
    metadata_sow_mother_son.replace(sow, sow_son, inplace=True)

metadata_time[1:] = metadata_animalID_sow["Animal ID"][1:].str[-2:]
# %% [markdown]
# #### Add the columns to the metadata
# %%
metadata["time"] = metadata_time
# neighboorhood already has the same shape of sow_son
# metadata["sow_son"] = metadata_sow_mother_son
metadata["sow"] = metadata_sow_mother


# %% [markdown]
#
# ### 2)PERCENTAGE
# Why am I conducting this study?
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
# Calculate the proportion of survived piglets for each row
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
# ### ARISING PROBLEM (Inconsistent Data)
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
#
# However, we can easily notice that the first three columns are correlated with time $T_0$.
# Therefore, the equation is defined as follows: ${nest} = {alive} + {dead}$.
#
# But also the number transferred are correlated with time $T_0$.
#
# Instead, we don't know at which time ${uw_el}$ is referred. Could it be piglets born underweight at time $T_0$? Or could they become underweight at time $T_1$ or later?
#
# However, the equations are defined as follows:
#
# - For the new number of alive piglets: `new_alive = alive - uw_el`.
#
#
# The problem arises when these equations are not respected. For example, we can have the following situation:
#
# Respected time T0:
#
# | nest      | alive    | dead   | transferred | uw_el  | time   |
# |-----------|----------|--------|-------------|--------|--------|
# | numeric   | numeric  | numeric| numeric     | numeric|category|
# | 23        | 19       | 4      | 2           | 2      |T0      |
#
# Not respected time T1:
#
# | nest      | alive    | dead   | transferred | uw_el  | time   |
# |-----------|----------|--------|-------------|--------|--------|
# | numeric   | numeric  | numeric| numeric     | numeric|category|
# | 23        | 19       | 4      | 2           | 2      |T1      |
#
# To be consistent, it should be like this (nest, for me, should be modified with alive due to the fact that in metadata it is specified that alive is the number of piglets alive in the nest at birth, so time T0, and the ones transferred at time T0):
#
# | nest      | alive    | dead   | transferred | uw_el  | time   |
# |-----------|----------|--------|-------------|--------|--------|
# | numeric   | numeric  | numeric| numeric     | numeric|category|
# | 17        | 19       | 4      | 2           | 2      |T0      |
#
# %% [markdown]

# #### Study on the Number of Piglets Eliminated Due to Underweight

# I created a proportion: $ \frac{nest_{piglets}}{100} = \frac{underweight_{piglets}}{underweight_{percentage}}$. Then, I divided the piglets into two groups: underweight and not underweight. In this case, I only considered piglets after time $T_0$.

# %%
metadata_nest_underweight = metadata[["alive", "uw_el", "time", "transferred"]]

perc_dead = metadata_nest_underweight[1:].apply(
    lambda x: (int(x["uw_el"]) * 100 / (int(x["alive"])) - int(x["transferred"]))
    if x["time"] != "T0"
    else 0,
    axis=1,
)

# Calculate mean_dead
somma = 0
count = 0
for i in range(1, len(perc_dead)):
    if metadata_nest_underweight["time"][i] != "T0":
        somma += perc_dead[i]
        count += 1

mean_dead = somma / count

# Modify metadata_dead based on mean_dead
metadata_dead = metadata["swab_ID"].copy()

for i in range(1, len(metadata_dead)):
    if perc_dead[i] < mean_dead and metadata_nest_underweight["time"][i] != "T0":
        metadata_dead[i] = "lot-of-underweight"
    elif metadata_nest_underweight["time"][i] != "T0":
        metadata_dead[i] = "few-underweight"
    else:
        metadata_dead[i] = "none"

metadata["underweight"] = metadata_dead

# %% [markdown]
# #### Study on the number of piglets transferred
# Just bring to 0 the transferred piglets aftere time T0
# %%
metadata_transferred = metadata["transferred"].copy()
metadata_transferred_time = metadata[["time", "transferred"]]

metadata_transferred[1:] = metadata_transferred_time[1:].apply(
    lambda x: 0 if x["time"] != "T0" else x["transferred"], axis=1
)

metadata["transferred"] = metadata_transferred

# %% [markdown]
# ### Drop uselss column by checking the correlation between some of the columns
# - **rename** the $neigh$ column to $cell$.
# - **Drop** $Animal \space ID$ defined as categorical split in $time$ and $sow$ and $sow_{son}$ the last one can also can be omitted due to the fact
# correspond as the same as the $cell$ column.
# - **Drop** $dead$ and $alive$ due to the fact that they are correlated with $nest$ and they seems redundant better usage of means and percentage as created before.
# - **Drop** $swab_{ID}$ due to the fact that it is a unique identifier and it is not useful for the analysis and also are present others unique identifier.
# - **Drop** $nest$ due to the fact that it is correlated with $dead$ and $alive$, and we calculate the difference for a big or small nest.

# %%
metadata.drop("Animal ID", axis=1, inplace=True)
metadata.drop("swab_ID", axis=1, inplace=True)
metadata.rename(columns={"neigh": "cell"}, inplace=True)
save_metadata(metadata, "piglets_metadata_modified_full1.tsv")
metadata.drop("dead", axis=1, inplace=True)
metadata.drop("nest", axis=1, inplace=True)
metadata.drop("alive", axis=1, inplace=True)
save_metadata(metadata, "piglets_metadata_modified_neglet_some2.tsv")

# %% [markdown]
# ### Save the metadata

# %%
