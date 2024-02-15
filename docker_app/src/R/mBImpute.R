#!/usr/bin/env Rscript
library(qiime2R)
library(mbImpute)
library(biomformat)
library(ape)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No arguments provided", call. = FALSE)
}
metadata <- args[1]


path_to_data <- paste0(getwd(), "/data")
print(path_to_data)
print("--> FOLDER CHECK")
filename_in <- paste0(path_to_data,"/3_feature_tables/feature_table.qza")
filename_out_imp <- paste0(path_to_data,"/3.1_feature_table_imp/feature_table_imp.biom")
filename_out_lgn <- paste0(path_to_data,"/3.3_feature_table_imp_lgn/feature_table_imp_lgn.biom")
filename_out_nrm <- paste0(path_to_data,"/3.2_feature_table_imp_nrm/feature_table_imp_nrm.biom")
filename_in_row <- paste0(path_to_data,"/3_feature_tables/feature_table.qza")
filename_metadata <- paste0(paste0(path_to_data,"/0_piglets_metadata/"), metadata)
base_tree_path <- paste0(path_to_data,"/tree/tree/")
all_items <- list.files(path = base_tree_path, full.names = TRUE, recursive = FALSE)
dirs <- all_items[sapply(all_items, function(x) file.info(x)$isdir)]
if (length(dirs) == 0) {
  stop("No subdirectories found in the specified path")
}
mod_times <- sapply(dirs, function(x) file.info(x)$mtime)
most_recent_dir <- dirs[which.max(mod_times)]
filename_tree <- file.path(most_recent_dir, "data/tree.nwk")
print("--> READ QZA")
features <- read_qza(filename_in)
input_matrix <-  features$data
print("--> READ METADATA")
meta_data <- read.csv(filename_metadata, sep="\t") 
study_condition <- meta_data[,'diarrhea']
meta_data <- as.data.frame(unclass(meta_data))
meta_data <- meta_data[ , !colnames(meta_data) %in% 'diarrhea']
print("--> READ TREE")
# COST EXPENSIVE NEED MORE RESOURCES
# tree <- read.tree(filename_tree)
# D <- cophenetic(tree)
print("--> SAVE .BIOM OF NO IMPUTED DATA")
row_data <- read_qza(filename_in_row)
taxa <- row_data$data
taxa <- as.data.frame(taxa)
write.csv(taxa, file = "/home/microbiome/data/3_feature_tables/feature_table.csv", row.names = FALSE)
print("--> LAUNCH IMPUTATION")
input_matrix_imp <- mbImpute(otu_tab = t(input_matrix),
                            condition = study_condition,
                            metadata = meta_data,
#                           D = D,
#                           k = 5, 
                            parallel = F, 
                            ncores = 1, 
#                           unnormalized = TRUE
)
print("--> SAVE .BIOM IMPUTED DATA")
taxa_imputed_lognorm<- make_biom(t(input_matrix_imp$imp_count_mat_lognorm))
taxa_imputed_norm <- make_biom(t(input_matrix_imp$imp_count_mat_norm))
taxa_imputed <- make_biom(t(input_matrix_imp$imp_count_mat_origlibsize))
print("--> WRITE .BIOM FILES")
write_biom(taxa_imputed, filename_out_imp)
write_biom(taxa_imputed_lognorm, filename_out_lgn)
write_biom(taxa_imputed_norm, filename_out_nrm)
print("--> CREATE .CSV FILES")
write.csv(t(as.data.frame(input_matrix_imp$imp_count_mat_origlibsize)), file = "/home/microbiome/data/3.1_feature_table_imp/feature_table_imp.csv", row.names = FALSE)
write.csv(t(as.data.frame(input_matrix_imp$imp_count_mat_lognorm)), file = "/home/microbiome/data/3.3_feature_table_imp_lgn/feature_table_imp_lgn.csv", row.names = FALSE)
write.csv(t(as.data.frame(input_matrix_imp$imp_count_mat_norm)), file = "/home/microbiome/data/3.2_feature_table_imp_nrm/feature_table_imp_nrm.csv", row.names = FALSE)
