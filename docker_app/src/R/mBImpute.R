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
distance_matix_yes_or_no <- args[2]
tree_type <- args[3]

path_to_data <- paste0(getwd(), "/data")
print("--> FOLDER CHECK")
filename_in <- paste0(path_to_data,"/3_feature_tables/feature_table.qza")
filename_out_imp <- paste0(path_to_data,"/3.1_feature_table_imp/feature_table_imp.biom")
filename_out_lgn <- paste0(path_to_data,"/3.3_feature_table_imp_lgn/feature_table_imp_lgn.biom")
filename_out_nrm <- paste0(path_to_data,"/3.2_feature_table_imp_nrm/feature_table_imp_nrm.biom")
filename_metadata <- paste0(paste0(path_to_data,"/0_piglets_metadata/"), metadata)

if (tree_type == "rooted") {
    filename_tree <- paste0(path_to_data, "/tree/tree_rooted.nwk")
}
if (tree_type == "unrooted") {
    filename_tree <- paste0(path_to_data, "/tree/tree_unrooted.nwk")
}
if (tree_type != "rooted" && tree_type != "unrooted") {
    stop("Tree type not recognized", call. = FALSE)
}

print("--> READ QZA")
features <- read_qza(filename_in)
input_matrix <-  features$data
input_matrix <- as.data.frame(input_matrix)
input_matrix <- t(input_matrix)
write.csv(t(input_matrix), file = "/home/microbiome/data/3_feature_tables/feature_table.csv", row.names = FALSE)

print("--> READ METADATA")
meta_data <- read.csv(filename_metadata, sep="\t") 
study_condition <- meta_data[,'diarrhea']
meta_data <- as.data.frame(unclass(meta_data))
meta_data <- meta_data[ , !colnames(meta_data) %in% 'diarrhea']

if (distance_matix_yes_or_no == "y"){
print("--> READ TREE")
tree <- read.tree(filename_tree)
distance_matrix <- cophenetic(tree)
write.csv(as.data.frame(distance_matrix), file = "/home/microbiome/data/3_feature_tables/Distance_matrix.csv", row.names = FALSE)
print("--> Checking shapes before mbImpute:")
print(paste("Shape of input_matrix (OTU table):", paste(dim(input_matrix), collapse = " x ")))
print(paste("Shape of D (distance matrix):", paste(dim(distance_matrix), collapse = " x ")))
colnames(distance_matrix) <- gsub("'", "", colnames(distance_matrix))
rownames(distance_matrix) <- gsub("'", "", rownames(distance_matrix))
not_in_distance_matrix <- setdiff(colnames(input_matrix), colnames(distance_matrix))

filtered_input_matrix <- input_matrix[, !(colnames(input_matrix) %in% not_in_distance_matrix)]

common_features <- intersect(colnames(filtered_input_matrix), colnames(distance_matrix))
filtered_input_matrix <- filtered_input_matrix[, common_features]
filtered_distance_matrix <- distance_matrix[common_features, common_features]
write.csv(as.data.frame(filtered_distance_matrix), file = "/home/microbiome/data/3_feature_tables/Filtered_distance_matrix.csv", col.names = FALSE)
write.csv(as.data.frame(t(filtered_input_matrix)), file = "/home/microbiome/data/3_feature_tables/Filtered_input_matrix.csv", col.names = FALSE)
print("--> Reshape of the distance matrix done:")
print(paste("Shape of input_matrix (OTU table):", paste(dim(filtered_input_matrix), collapse = " x ")))
print(paste("Shape of D (distance matrix):", paste(dim(filtered_distance_matrix), collapse = " x ")))
input_matrix <- t(filtered_input_matrix)
print("--> LAUNCH IMPUTATION WITH TREES")
input_matrix_imp <- mbImpute(otu_tab = t(input_matrix),
                               condition = study_condition,
                               metadata = meta_data,
                               D = filtered_distance_matrix,
                               parallel = F, 
                               ncores = 1 
                               )
}

if (distance_matix_yes_or_no == "n"){
  print("--> LAUNCH IMPUTATION WITHOUT DISTANCE MATRIX")
  input_matrix_imp <- mbImpute(otu_tab = t(input_matrix),
                               condition = study_condition,
                               metadata = meta_data,
                               parallel = F, 
                               ncores = 1 
                               )
}

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