#!/usr/bin/env Rscript

# CLR normalization
library(compositions)
library(qiime2R)
library(biomformat)
source("/home/microbiome/src/utilities.R")

# Set the directory
dir <- "/home/microbiome/data"

# take the name of the first element given
taxatype <- commandArgs(TRUE)[1]

print("CLR normalization STARTED")

# Importing
filename_in <- paste(taxatype, "_table_norm", sep = "")
taxa_ls <- take_specific_qza(dir, filename_in)

# Save the asv matrix:
taxa_table <- taxa_ls$data

# CLR normalization:
taxa_table_clr <- compositions::clr(taxa_table, )

# create biom file in the folder :
taxa_biom <- make_biom(taxa_table_clr)

setwd(dir)
list_folder <- create_folder_name_and_file("10", taxatype, "clr_table_norm")
folder_name <- list_folder[[1]]
filename_out <- list_folder[[2]]
print("folder name:")
print(folder_name)
print("filename out:")
print(filename_out)

if (!dir.exists(folder_name)) {
    dir.create(folder_name)
}

setwd(paste(dir, "/", folder_name, sep = ""))
write_biom(taxa_biom, paste0(filename_out, ".biom"))

print(sprintf("CLR normalization %s ENDED store in %s", filename_out, folder_name))
