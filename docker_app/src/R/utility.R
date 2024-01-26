library(qiime2R)
library(biomformat)
library(tibble)
library(dplyr)

# Function to take the qza file
#
#' @param data_path: path of the data
#' @param grep_pattern_folder: pattern to find the qza file "table_norm"
#' @param specific_qza_grep: pattern to find the qza file "table_norm.qza"
#' @return qza_file: qza file
#' @example take_specific_qza("/home/microbiome/data", "table_norm", "table_norm.qza") returns qza file # nolint: line_length_linter.
#'
take_specific_qza <- function(data_path, grep_pattern_folder, specific_qza_grep = "") {
  folders <- list.files(data_path, full.names = TRUE)
  count <- 0
  qza_file <- NULL
  for (folder in folders) {
    if (grepl(grep_pattern_folder, folder)) {
      count <- count + 1
      print(sprintf("--> FOLDER %s ", folder))
      files <- list.files(folder, pattern = "*.qza", full.names = TRUE)

      if (count > 1) {
        print("Selected more then one folder the grep does not work")
        break
      }

      if (specific_qza_grep == "") {
        if (length(files) > 0) {
          qza_file <- qiime2R::read_qza(files[1])
        } else {
          print(".qza file empty ")
        }
      } else {
        if (length(files) > 0) {
          for (file in files) {
            if (grepl(specific_qza_grep, file)) {
              qza_file <- qiime2R::read_qza(file)
            }
          }
        }
      }
    }
  }
  return(qza_file)
}

# Function to take the biom file
#
#' @param data_path: path of the data
#' @param grep_pattern_folder: pattern to find the biom file "table_norm"
#' @return biom_file: biom file
#' @example take_specific_bioformat("/home/microbiome/data", "table_norm") returns biom file # nolint: line_length_linter.

take_specific_bioformat <- function(data_path, grep_pattern_folder) {
  folders <- list.files(data_path, full.names = TRUE)
  count <- 0
  biom_file <- NULL

  for (folder in folders) {
    if (grepl(grep_pattern_folder, folder)) {
      count <- count + 1
      print(sprintf("Folder--> %s ", folder))
      files <- list.files(folder, pattern = "*.biom", full.names = TRUE)

      if (count > 1) {
        print("Selected more than one folder")
        break
      }

      if (length(files) > 0) {
        biom_file <- biomformat::read_biom(files[1])
      } else {
        cat(".biom file is empty.")
      }
    }
  }
  return(biom_file)
}

# Function to take the metadata
#
#' @param data_path: path of the data
#' @param grep_pattern_folder: pattern to find the metadata "metadata"
#' @param grep_pattern_metadata: pattern to find the metadata "metadata.tsv"
#' @return meta_data: metadata
#' @example take_meta_data("/home/microbiome/data", "metadata", "metadata.tsv") returns metadata # nolint: line_length_linter.

take_meta_data <- function(data_path, grep_pattern_folder, grep_pattern_metadata = "") {
  folders <- list.files(data_path, full.names = TRUE)
  count <- 0
  meta_data <- NULL

  for (folder in folders) {
    if (grepl(grep_pattern_folder, folder)) {
      count <- count + 1
      print(sprintf("Folder--> %s ", folder))
      files <- list.files(folder, pattern = "*.tsv", full.names = TRUE)

      if (count > 1) {
        print("Selected more than one folder")
        break
      }
      # if the grep pattern is empty take the first file
      if (grep_pattern_metadata == "") {
        if (length(files) > 0) {
          meta_data <- read.table(files[1], sep = "\t", header = TRUE)
        } else {
          cat(".tsv file is empty.")
        }
        # if the grep pattern is not empty take the file with the pattern
      } else {
        if (length(files) > 0) {
          for (file in files) {
            if (grepl(grep_pattern_metadata, file)) {
              meta_data <- read.table(file, sep = "\t", header = TRUE)
            }
          }
        }
      }
      meta_data <- read.table()
    }
  }
  return(meta_data)
}

# Function to create string with the number of the folder and taxatype
#
#' @param number_of_folder Number of the folder (e.g., 9)
#' @param taxatype Type of taxa (e.g., asv, genus, species)
#' @param folder_name Name of the folder (e.g., "table_norm_GMRP")
#' @return A list containing the folder name and file name
#' @example first_number_folder(1, "asv", "table_norm_GMRP") returns a list with folder and file names # nolint

create_folder_name_and_file <- function(number_of_folder, taxatype, folder_name) {
  file_name <- paste(taxatype, folder_name, sep = "_")
  if (taxatype == "asv") {
    folder_number <- paste(number_of_folder, "1", sep = ".")
  } else if (taxatype == "genus") {
    folder_number <- paste(number_of_folder, "2", sep = ".")
  } else if (taxatype == "species") {
    folder_number <- paste(number_of_folder, "3", sep = ".")
  } else {
    print("taxatype not correct")
  }
  folder_name <- paste(folder_number, file_name, sep = "_")

  return(list(folder_name = folder_name, file_name = file_name))
}
filter_metadata_and_counts <- function(metadata_path, count_table_path, column_name, column_values) {
    # Import metadata and set row names
    metadata <- read_q2metadata(metadata_path)
    metadata_df <- data.frame(metadata[, -1], row.names = metadata[, 1]) # Set sample ID as row names
    metadata_df[metadata_df == ""] <- NA # Convert empty strings to NA

    # Filter metadata based on column values
    filtered_metadata_list <- list()
    print("--> Filtering the metadata based on the column name")
    for (value in column_values) {
        print(paste("Filtering metadata for value", value))
        new_metadata <- metadata_df[metadata_df[[column_name]] %in% value, ]
        filtered_metadata_list <- append(filtered_metadata_list, list(new_metadata))
    }

    # Merge the filtered metadata
    print("--> Merging the filtered metadata, and transforming it into a data frame")
    filtered_metadata <- do.call(rbind, filtered_metadata_list)

    # Import and transpose the count table
    print("--> Importing the count table")
    count_table_data <- read_qza(count_table_path) 
    count_table <- t(count_table_data$data)
    count_table <- as.data.frame(count_table)
    count_table[count_table == ""] <- NA
    sample_ids <- rownames(filtered_metadata)
    if (!all(sample_ids %in% rownames(count_table))) {
        stop("Some metadata sample IDs are not present in count table column names.")
    }
    filtered_count_table <- count_table[rownames(filtered_metadata), ]
    print("--> Write the dataframes on the disk")

    return(list("FilteredMetadata" = filtered_metadata, "FilteredCountTable" = filtered_count_table))
}

