#!/usr/bin/env Rscript
library(qiime2R)
library(Maaslin2)
source("/home/microbiome/docker_app/src/R/utility.R")
# Define your functions here (take_specific_qza, take_specific_bioformat, take_meta_data, create_folder_name_and_file, filter_metadata_and_counts)

# Function to parse command line arguments
parse_args <- function(args) {
    options <- list()
    current_arg <- NULL
    for (arg in args) {
        if (startsWith(arg, "-")) {
            current_arg <- substring(arg, 2)
            options[[current_arg]] <- NULL
        } else if (!is.null(current_arg)) {
            options[[current_arg]] <- arg
            current_arg <- NULL
        }
    }
    return(options)
}

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
options <- parse_args(args)
taxa <- options[["taxa"]]
norm <- options[["norm"]]
outcome <- options[["outcome"]]
tsv_file <- options[["tsv"]]
metadata_name <- options[["metadata"]]
list_random <- strsplit(options[["list_random"]], ",")[[1]]
column_name <- options[["column_name"]]
list_column_value <- strsplit(options[["list_column_value"]], ",")[[1]]

# Print the parsed arguments
print(paste("--> Taxa:", taxa))
print(paste("--> Normalization:", norm))
print(paste("--> Outcome:", outcome))
print(paste("--> TSV file:", tsv_file))
print(paste("--> List Random:", paste(list_random, collapse = ", ")))
print(paste("--> Column name:", column_name))
print(paste("--> List column value:", paste(list_column_value, collapse = ", ")))

# Define directories and filenames
taxa_ids <- c(asv = 1, genus = 2, species = 3)
id <- taxa_ids[taxa]
dir <- "/home/microbiome/data"
output_base_dir <- paste0(dir, "/9.", id, "_", taxa, "_", norm, "_DA_MaAsLin2")
filename_in <- paste0(dir, "/6.", id, "_", taxa, "_", norm, "_table_norm/", taxa, "_", norm, "_table_norm.qza")
path_metadata <- paste0(dir, "/0_piglets_metadata/", tsv_file)

setwd(dir)


result <- filter_metadata_and_counts(path_metadata, filename_in, column_name, list_column_value)
print("--> Importing the metadata")
filtered_metadata <- result$FilteredMetadata
print("--> Importing the count table")
filtered_count_table <- result$FilteredCountTable

# After importing the metadata and count table
print("--> After Importing Data")
print("Dimensions of the filtered metadata:")
print(dim(filtered_metadata))
print("First few rows of metadata:")
print(head(rownames(filtered_metadata)))

print("Dimensions of the filtered count table:")
print(dim(filtered_count_table))
print("First few columns of count table:")
print(colnames(filtered_count_table)[1:10]) # adjust to see more if needed

# Check if the number of rows in metadata matches the number of columns in count table
if (nrow(filtered_metadata) == ncol(filtered_count_table)) {
  print("Row count of metadata matches column count of count table.")
} else {
  print("Mismatch in row count of metadata and column count of count table.")
  print("Metadata rows:")
  print(nrow(filtered_metadata))
  print("Count table columns:")
  print(ncol(filtered_count_table))
}

# Check if the row names of metadata match the column names of count table
if (all(rownames(filtered_metadata) %in% colnames(filtered_count_table))) {
  print("All metadata row names are present in count table column names.")
} else {
  print("Some metadata row names are not present in count table column names.")
  print("Missing names:")
  print(setdiff(rownames(filtered_metadata), colnames(filtered_count_table)))
}

# Check for any NA or empty values in row names and column names
if (any(is.na(rownames(filtered_metadata))) || any(rownames(filtered_metadata) == "")) {
  print("There are NA or empty row names in the metadata.")
}
if (any(is.na(colnames(filtered_count_table))) || any(colnames(filtered_count_table) == "")) {
  print("There are NA or empty column names in the count table.")
}

# Additional check for data types
print("Data types in metadata:")
print(sapply(filtered_metadata, class))
print("Data types in count table:")
print(sapply(filtered_count_table, class))

# Add these lines right before the Maaslin2 function call


print("--> Running Maaslin2")
fit_data <- Maaslin2(
    input_data = filtered_count_table,
    input_metadata = filtered_metadata,
    fixed_effects = outcome,
    output = output_base_dir,
    random_effects = list_random,
    min_prevalence = 0.001,
    min_abundance = 0.00001
)

print("--> Differential Abundance analysis ENDED")
