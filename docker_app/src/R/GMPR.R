#!/usr/bin/env Rscript

# GMPR normalization
library(GMPR)
library(qiime2R)
library(biomformat)
source("/home/microbiome/docker_app/src/R/utility.R")

# Set the directory
dir <- "/home/microbiome/data"

# Take the name of the first element given
taxatype <- commandArgs(TRUE)[1]

print("GMPR normalization STARTED")

# Importing
filename_in <- paste(taxatype, "_table_taxafilt", sep = "")
taxa_ls <- take_specific_qza(dir, filename_in)

taxa_table <- taxa_ls$data
taxa_table <- t(taxa_table)
taxa_table <- as.data.frame(taxa_table)
GMPR_factors <- GMPR(OTUmatrix = taxa_table)
print("GMPR factors:")
print(GMPR_factors)
taxa_table_norm <- t(taxa_table / GMPR_factors)
taxa_table_norm[is.na(taxa_table_norm)] <- 0

# Create directory or clear it if it already exists
list_folder <- create_folder_name_and_file("10", taxatype, "gmpr_table_norm")
folder_name <- list_folder[[1]]
folder_path <- paste(dir, "/", folder_name, sep = "")

if (!dir.exists(folder_path)) {
  dir.create(folder_path)
} else {
  file.remove(list.files(folder_path, full.names = TRUE))
}

# Change working directory to the created folder
setwd(folder_path)

# Construct file paths for CSV files
original_csv_path <- paste0(getwd(), "/", taxatype, "_original_taxa_table.csv")
normalized_csv_path <- paste0(getwd(), "/", taxatype, "_normalized_taxa_table.csv")

# Save original and normalized taxa tables to CSV in the created folder
write.csv(taxa_table, file = original_csv_path, row.names = FALSE)
write.csv(taxa_table_norm, file = normalized_csv_path, row.names = FALSE)

# Create biom file and save it
taxa_biom <- make_biom(taxa_table_norm)
write_biom(taxa_biom, paste0(taxatype, "_gmpr_table_norm.biom"))


