#!/usr/bin/env Rscript

library(GMPR)
library(qiime2R)
library(biomformat)
source("/home/microbiome/docker_app/src/R/utility.R")

taxatype <- commandArgs(TRUE)[1]

print("GMPR normalization STARTED")

filename_in <- paste(taxatype, "_table_taxafilt", sep = "")
dir <- "/home/microbiome/data"

taxa_ls <- take_specific_qza(dir, filename_in)
taxa_table <- taxa_ls$data

# Transpose the table to apply GMPR by features
taxa_table_transposed <- t(taxa_table)

# Apply GMPR on the transposed table (features)
GMPR_factors <- GMPR::GMPR(OTUmatrix = as.data.frame(taxa_table_transposed))
print(GMPR_factors)

# Normalize and then transpose back
taxa_table_norm <- t(as.data.frame(taxa_table_transposed) / GMPR_factors)

list_folder <- create_folder_name_and_file("6", taxatype, "gmpr_table_norm")
folder_name <- list_folder[[1]]
folder_path <- paste(dir, "/", folder_name, sep = "")
print(folder_path)
setwd(folder_path)

taxa_biom <- make_biom(taxa_table_norm)
write_biom(taxa_biom, paste0(taxatype, "_gmpr_table_norm.biom"))

original_csv_path <- paste0(getwd(), "/", taxatype, "_original_taxa_table.csv")
normalized_csv_path <- paste0(getwd(), "/", taxatype, "_normalized_taxa_table.csv")
write.csv(taxa_table, file = original_csv_path, row.names = FALSE)
write.csv(taxa_table_norm, file = normalized_csv_path, row.names = FALSE)
