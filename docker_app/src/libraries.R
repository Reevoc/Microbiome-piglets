#!urs/bin/env Rscript
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools")
}

library(devtools)
if (!requireNamespace("compositions", quietly = TRUE)) {
  install.packages("compositions")
}
library(compositions)

if (!requireNamespace("installr", quietly = TRUE)) {
  install.packages("installr")
}
library(installr)

if (!require("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
library(BiocManager)

BiocManager::install("biomformat")
library(biomformat)

# Install rmarkdown package
if (!requireNamespace("rmarkdown", quietly = TRUE)) {
  install.packages("rmarkdown")
}

# Load rmarkdown package
library(rmarkdown)

# Install GMPR normalization package
install_github("lichen-lab/GMPR")
install_github("jbisanz/qiime2R")
