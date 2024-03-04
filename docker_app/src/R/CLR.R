#!/usr/bin/env Rscript
library(compositions)
library(qiime2R)
library(biomformat)
source("/home/microbiome/docker_app/src/R/utility.R")

# Set the directory
dir <- "/home/microbiome/data"

# Take the name of the first element given
taxatype <- commandArgs(TRUE)[1]

print("--> CLR STARTED")

# Importing
filename_in <- paste(taxatype, "_table_taxafilt", sep = "")
taxa_ls <- take_specific_qza(dir, filename_in)

taxa_table <- taxa_ls$data

taxa_table[taxa_table == 0] <- 1

taxa_table_clr <- compositions::clr(compositions::acomp(taxa_table))

taxa_table_clr[is.na(taxa_table_clr) | is.infinite(taxa_table_clr)] <- 0

list_folder <- create_folder_name_and_file("6", taxatype, "clr_table_norm")
folder_name <- list_folder[[1]]
folder_path <- paste(dir, "/", folder_name, sep = "")

if (!dir.exists(folder_path)) {
  dir.create(folder_path)
} else {
  file.remove(list.files(folder_path, full.names = TRUE))
}

setwd(folder_path)

normalized_csv_path <- paste0(getwd(), "/", taxatype, "_normalized_taxa_table.csv")
original_csv_path <- paste0(getwd(), "/", taxatype, "_original_taxa_table.csv")
write.csv(taxa_table_clr, file = normalized_csv_path, row.names = FALSE)
write.csv(taxa_table, file = original_csv_path, row.names = FALSE)

taxa_biom <- make_biom(taxa_table_clr)
write_biom(taxa_biom, paste0(taxatype, "_clr_table_norm.biom"))

print("--> CLR END")
