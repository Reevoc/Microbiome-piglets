#!/usr/bin/env Rscript
library(Maaslin2)
library(qiime2R)
print("Differential Abundance analysis STARTED MasLin2")

# Rscript DA_MasLin2.R -taxa asv -norm clr -outcome n -tsv piglets_modified_small.tsv -list_random "is_sow,time,sex"

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

args <- commandArgs(trailingOnly = TRUE)
options <- parse_args(args)
taxa <- options[["taxa"]]
norm <- options[["norm"]]
outcome <- options[["outcome"]]
tsv_file <- options[["tsv"]]
metadata_name <- options[["metadata"]]
list_random <- strsplit(options[["list_random"]], ",")[[1]]

print(paste("Taxa:", taxa))
print(paste("Normalization:", norm))
print(paste("Outcome:", outcome))
print(paste("TSV file:", tsv_file))
print(paste("List Random:", paste(list_random, collapse = ", ")))

taxa_ids <- c(asv = 1, genus = 2, species = 3)
id <- taxa_ids[taxa]
id <- switch(taxa,
    asv = 1,
    genus = 2,
    species = 3,
    NA
)

dir <- "/home/piermarco/Documents/Thesis/data"
output_base_dir <- paste0(
    dir, "/14.",
    id, "_", taxa,
    "_", norm,
    "DA_MaAsLin2"
)

filename_in <- paste0(
    dir, "/10.", id,
    "_", taxa, "_",
    norm, "_table_norm/",
    taxa, "_",
    norm, "_table_norm.qza"
)

path_metadata <- paste0(dir, "/0.2_piglets_metadata/", tsv_file)

print("Set the directory")
setwd(dir)

print("Importing the metadata")
metadata <- read_q2metadata(path_metadata)
input_metadata <- data.frame(metadata[, -1], row.names = metadata[, 1])
input_metadata[input_metadata == ""] <- NA
input_metadata <- as.data.frame(input_metadata)
unique(input_metadata$diarrhea)
input_metadata$diarrhea_modified <- input_metadata$diarrhea
input_metadata$diarrhea_modified <- factor(input_metadata$diarrhea_modified,
    levels = c("y", "n", "e")
)

print("Importing the qza file")
features <- read_qza(filename_in)
input_matrix <- features$data
input_matrix <- input_matrix[, as.character(metadata$SampleID)]
input_matrix <- input_matrix[rowSums(input_matrix) != 0, ]
input_matrix <- as.data.frame(t(input_matrix))

print("Start Maaslin2")
fit_data <- Maaslin2(
    input_data = input_matrix,
    input_metadata = input_metadata,
    fixed_effects = c("diarrhea_modified"),
    output = output_base_dir,
    random_effects = list_random,
    min_prevalence = 0.01,
    min_abundance = 0.0001
)

print("Differential Abundance analysis ENDED")
