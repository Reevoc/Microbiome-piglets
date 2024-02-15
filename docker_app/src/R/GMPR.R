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
taxa_table <- t(taxa_table)
taxa_table <- as.data.frame(taxa_table)
GMPR_factors <- GMPR(OTUmatrix = taxa_table)
print("GMPR factors:")
taxa_table_norm <- t(taxa_table / GMPR_factors)
taxa_table_norm[is.na(taxa_table_norm)] <- 0

list_folder <- create_folder_name_and_file("6", taxatype, "gmpr_table_norm")
folder_name <- list_folder[[1]]
folder_path <- paste(dir, "/", folder_name, sep = "")

if (!dir.exists(folder_path)) {
  dir.create(folder_path)
} else {
  file.remove(list.files(folder_path, full.names = TRUE))
}

setwd(folder_path)

original_csv_path <- paste0(getwd(), "/", taxatype, "_original_taxa_table.csv")
normalized_csv_path <- paste0(getwd(), "/", taxatype, "_normalized_taxa_table.csv")

write.csv(taxa_table, file = original_csv_path, row.names = FALSE)
write.csv(taxa_table_norm, file = normalized_csv_path, row.names = FALSE)

taxa_biom <- make_biom(taxa_table_norm)
write_biom(taxa_biom, paste0(taxatype, "_gmpr_table_norm.biom"))


