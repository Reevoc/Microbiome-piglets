#!/usr/bin/env Rscript
library(qiime2R)
library(mbImpute)
library(biomformat)
setwd("/home/microbiome/data")
# Get arguments from the command line
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No arguments provided", call. = FALSE)
}
if (length(args) < 2) {
  stop("At least two arguments are required", call. = FALSE)
}
metadata <- args[1]
print(paste("--> Metadata :", metadata))
meta_data_path <- paste0("/0_metadata_piglets/", metadata, ".tsv")
meta_data <- read.csv(meta_data_path)
print("--> FOLDER CHECK")
filename_in <- "/3_feature_tables/feature_table.qza"
filename_out_imp <- "/3.1_feature_table_imp/feature_table_imp.biom"
filename_out_lng <- "/3.2_feature_table_imp_lng/feature_table_imp_lng.biom"
filename_out_nrm <- "/3.3_feature_table_imp_nrm/feature_table_imp_nrm.biom" 
filename_metadata <-- paste0("/0_piglets_metadata/", metadata)
print("--> READ QZA")
features <- read_qza(filename_in)
input_matrix <-  features$data
study_condition <- meta_data[,'diarrhea']
meta_data <- as.data.frame(unclass(meta_data))
meta_data <- meta_data[,-'diarrhea'] 
print("--> LAUNCH IMPUTATION")
input_matrix_imp <- mbImpute(otu_tab = t(input_matrix),
                            condition = study_condition,
                            meta_data = meta_data,
                            D = D,
                            k = 5, 
                            parallel = F, 
                            ncores = 1, 
                            unnormalized = FALSE)
print("--> SAVE .BIOM")
taxa_imputed_lognorm<- make_biom(t(input_matrix_imp$imp_count_mat_lognorm))
taxa_imputed_norm <- make_biom(t(input_matrix_imp$imp_count_mat_norm))
taxa_imputed <- make_biom(t(input_matrix_imp$imp_count_mat_origlibsize))
write_biom(taxa_imputed, filename_out_imp)
write_biom(taxa_imputed_lognorm, filename_out_lng)
write_biom(taxa_imputed_norm, filename_out_nrm)
