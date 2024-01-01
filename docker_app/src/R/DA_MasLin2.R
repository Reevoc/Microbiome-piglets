#!/usr/bin/env Rscript
setwd("/path/to/your/directory") # Update this to your working directory

print("Differential Abundance analysis STARTED")
rm(list = ls())

# Define your parameters here
taxatype <- "Your_Taxa_Type" # Replace with your taxa type
fixedeff <- "diarrhea" # Using 'diarrhea' as the condition for analysis

library(qiime2R)

# Import metadata
metadata <- read_q2metadata("/path/to/your/metadata.tsv") # Path to your metadata file

# Filter metadata based on the presence of diarrhea e and y
metadata <- metadata[metadata$diarrhea == "e", ] # Selects samples with diarrhea

# Generate group labels
group_labels <- as.character(metadata$diarrhea)
sex_labels <- as.character(metadata$sex)
sow_labels <- as.vector(metadata$is_sow) # Assuming sample-id reflects age or other relevant info

labels_df <- data.frame("group" = group_labels, "sex" = sex_labels, "age" = age_labels, stringsAsFactors = FALSE)
input_metadata <- data.frame(metadata[, -1], row.names = metadata[, 1]) # Adapt as per your metadata structure
input_metadata[input_metadata == ""] <- NA

# Load feature table
filename_in <- paste0("/path/to/your/", taxatype, "_table_norm.qza")
features <- read_qza(filename_in)
input_matrix <- features$data

# Process the matrix as per your analysis requirements
input_matrix <- input_matrix[, as.character(metadata$sample - id)]
input_matrix <- input_matrix[rowSums(input_matrix) != 0, ]
input_data <- as.data.frame(input_matrix)

# Load MaAsLin2 package
library(Maaslin2)

# Run MaAsLin2 for DA analysis
fit_data <- Maaslin2(
    input_data = input_data,
    input_metadata = input_metadata,
    min_prevalence = 0.01, # Adjust as needed
    normalization = "NONE",
    output = paste0("/path/to/output/DA_output/MaAsLin2_", taxatype, "_", fixedeff),
    fixed_effects = c(fixedeff), # Adapt based on your study
    random_effects = c("age", "sex"), # Adapt based on your study
    reference = c("n") # Reference condition for 'diarrhea'
)

print("Differential Abundance analysis ENDED")
