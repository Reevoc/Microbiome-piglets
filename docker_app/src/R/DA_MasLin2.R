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
filtered_metadata <- result$FilteredMetadata
filtered_count_table <- t(result$FilteredCountTable)

#print("--> Dimensions of the filtered metadata:")
#print(dim(filtered_metadata))
#print("--> First few rows of metadata:")
#print(rownames(filtered_metadata)[1:5])
#print("--> First few columns of metadata:")
#print(colnames(filtered_metadata)[1:5]) 
#
#print("--> Dimensions of the filtered count table:")
#print(dim(filtered_count_table))
#print("--> First few rows of count table:")
#print(rownames(filtered_count_table)[1:5])
#print("--> First few columns of count table:")
#print(colnames(filtered_count_table)[1:5])

print("--> Running Maaslin2")
fit_data <- Maaslin2(
    input_data = filtered_count_table,
    input_metadata = filtered_metadata,
    output = output_base_dir,
    fixed_effects = c("diarrhea"), # replace with your actual fixed effects
    random_effects = list_random, # if you have any random effects
    #normalization = "NONE", # or your chosen normalization method
    reference = c("diarrhea,n"), # setting 'n' as the reference level for 'diarrhea'
    max_significance = 0.01
)

print("--> Differential Abundance analysis ENDED")
