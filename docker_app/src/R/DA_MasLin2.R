#!/usr/bin/env Rscript
library(qiime2R)
library(Maaslin2)

dir <- "/home/microbiome/data"
setwd(dir) # Update this to your working directory

print("Differential Abundance analysis STARTED MasLin2")
rm(list = ls())

taxatype <- "asv" # commandArgs(TRUE)[1]
fixedeff <- "OPS" # commandArgs(TRUE)[2]
metadata_name <- "piglets_modified_small.tsv" # commandArgs(TRUE)[3]

if (taxatype == "asv") {
    id <- 1
}
if (taxatype == "genus") {
    id <- 2
}
if (taxatype == "species") {
    id <- 3
}

metadata <- read_q2metadata(paste0("/home/microbiome/data/0.2_pigles_metadata/", metadata_name)) # Path to your metadata file

input_metadata <- data.frame(metadata[, -1], row.names = metadata[, 1])
input_metadata[input_metadata == ""] <- NA

filename_in <- paste0("/home/microbiome/data/8.", id, "_asv_table_taxafilt/", taxatype, "_table_taxafilt.qza")
features <- read_qza(filename_in)
input_matrix <- features$data
input_data <- as.data.frame(input_matrix)

# Run MaAsLin2 for Differential Abundance analysis
fit_data <- Maaslin2(
    input_data = input_data, # Replace with your actual data file path
    input_metadata = input_metadata, # Replace with your actual metadata file path
    normalization = "clr",
    output = paste0("/path/to/output/DA_output/MaAsLin2_", fixedeff),
    fixed_effects = c("diarrhea", "sex", "gestations", "alive"),
    random_effects = c("time", "is_sow"),
    min_prevalence = 0.01,
    min_abundance = 0.0001,
)

print("Differential Abundance analysis ENDED")
