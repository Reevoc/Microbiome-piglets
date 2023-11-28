library(qiime2R)
library(biomformat)

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
      print(sprintf("Folder--> %s ", folder))
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
