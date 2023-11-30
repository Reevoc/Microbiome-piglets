# Microbiome_piglets

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following software installed:

- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
- [Docker](https://www.docker.com/)

### Clone the Repository

1. Navigate to the directory where you want to download the project:

   ```bash
   cd /your/path/to/repository
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/Reevoc/Microbiome_piglets.git
   ```

### Installing Docker App [Bioconductor Docker](https://hub.docker.com/r/bioconductor/bioconductor_docker/)

Follow these steps to set up the Docker environment:

1. [Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
   - Verify the installation:

      ```bash
      docker --help
      ```

      or check the version:

      ```bash
      docker --version
      ```

2. Build the Docker image (ensure you are in the correct directory before building):

   ```bash
   docker build -t microbiome_piglets .
   ```

3. Run the Docker image:

   ```bash
   docker run -e PASSWORD=pass -p 8787:8787 -d microbiome_piglets
   ```

4. Clone the useful GitHub repository downloaded locally into the Docker image:

   ```bash
   docker cp /your/path/to/Microbiome_piglets/docker_app/ CONTAINER_ID:/home/microbiome
   ```

   - Replace `CONTAINER_ID` with the ID of the Docker container, which you can find using:

      ```bash
      docker ps
      ```

5. Change into the project directory:

   ```bash
   cd /your/path/to/Microbiome_piglets/docker_app
   ```

6. Download the "data.zip" file from [Google Drive](https://drive.google.com/file/d/1Kx87HDn-XSEu_YU5cFvs7jH2YGkJLU-w/view?usp=drive_link) and unzip it in the same directory as the Docker image:

   ```bash
   cd path/to/your/download_where_data.zip
   unzip data.zip
   rm data.zip
   ```

7. Copy the data inside the Docker image:

   ```bash
   docker cp /your/path/to/Microbiome_piglets/docker_app/data/ CONTAINER_ID:/home/microbiome
   ```

   - Replace `CONTAINER_ID` with the ID of the Docker container, which you can find using:

      ```bash
      docker ps
      ```

8. Run the Docker image:

   ```bash
   docker exec -it <container_id_or_name> /bin/bash
   ```

   - Replace `<container_id_or_name>` with the ID or name of the Docker container, which you can find using:

      ```bash
      docker ps
      ```

### Installing View App

Follow these steps to set up the View environment:

1. Change into the project directory:

   ```bash
   cd /your/path/to/Microbiome_piglets
   ```

2. Install Mamba (an improved version of Conda):

   ```bash
   conda install -c conda-forge mamba
   ```

3. Create the Conda environment:

   ```bash
   wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml
   conda env create -n qiime2-amplicon-2023.9 --file qiime2-amplicon-2023.9-py38-linux-conda.yml
   rm qiime2-amplicon-2023.9-py38-linux-conda.yml
   ```

4. Activate the Conda environment (only needed for local viewing on your computer):

   ```bash
   conda activate qiime2-amplicon-2023.9
   ```

5. Use the view script to see the results:

   ```bash
   cd Microbiome_piglets/view
   bash view_app.sh
   ```
## QIIME 2: Core Concepts

### Data Files: QIIME 2 Artifacts
QIIME 2 utilizes artifacts to store data and metadata, offering a comprehensive representation of information. Artifacts, typically saved with a **.qza extension**, encompass details like data type, format, and provenance. By working with artifacts instead of conventional data files, researchers can streamline analyses, allowing a focus on analytical aspects without being constrained by specific data formats.

Artifacts facilitate automatic tracking of data lineage, ensuring **reproducibility and simplifying collaboration**. The decentralized provenance tracking system allows researchers to understand precisely how artifacts were generated, supporting proper attribution to underlying tools used in the analysis.

### Data Files: Visualizations
Visualizations in QIIME 2, denoted by **.qzv file extensions**, serve as terminal outputs showcasing results such as statistical tables, interactive visualizations, or static images. Unlike artifacts, **visualizations cannot be used as inputs for subsequent analyses but provide standalone, shareable information with embedded provenance data**.

### Semantic Types
Every QIIME 2 artifact is associated with a semantic type, enabling the software to identify suitable inputs for analyses. Semantic types prevent incompatible artifacts from being used in certain analyses, ensuring semantic correctness and meaningful results.

Visit the semantic types page for comprehensive information on available types and their applications.

### Plugins
QIIME 2 functionality is delivered through plugins, offering a modular approach to microbiome analyses. Users install plugins, such as **q2-demux** or **q2-diversity**, to access specific analyses. While the QIIME 2 team develops official plugins, third-party developers are encouraged to create additional plugins, fostering a decentralized ecosystem for diverse analyses.

Check the plugin availability page to explore the current offerings and the future plugins page for upcoming developments.

### Methods and Visualizers
QIIME 2 plugins define methods and visualizers for conducting analyses. Methods accept artifacts and parameters as input, producing one or more artifacts as output. Visualizers, on the other hand, produce a single visualization as terminal output. These components form the building blocks of QIIME 2 analyses, offering flexibility and customization.

*© Copyright 2016-2022, QIIME 2 development team. Created using Sphinx 5.3.0.*


## Ideas Behind the analysis
The data where give with the first part of preprocessing to me, so I didn't do any preprocessing. The data was already filtered and denoised. But to have a better understanding of the data I will explain the steps of preprocessing.
I first of all devided the data into folder, the dolder are numbered and followed by what kind of process was done on the data.

### 0.1) Piglets Manifest

Here is a small snippet of the first 5 rows of the dataset to give you an overview:


| sample-id                  | forward-absolute-filepath                                                  | reverse-absolute-filepath                                                  |
|----------------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------|
| 1450087F1381048_S1_L001    | $PWD/original_data/Raw_data/1450087F1381048_S1_L001_R1_001.fastq.gz     | $PWD/original_data/Raw_data/1450087F1381048_S1_L001_R2_001.fastq.gz     |
| 1450088F1381049_S2_L001    | $PWD/original_data/Raw_data/1450088F1381049_S2_L001_R1_001.fastq.gz     | $PWD/original_data/Raw_data/1450088F1381049_S2_L001_R2_001.fastq.gz     |
| 1450089F1381050_S3_L001    | $PWD/original_data/Raw_data/1450089F1381050_S3_L001_R1_001.fastq.gz     | $PWD/original_data/Raw_data/1450089F1381050_S3_L001_R2_001.fastq.gz     |
| 1450090F1381051_S4_L001    | $PWD/original_data/Raw_data/1450090F1381051_S4_L001_R1_001.fastq.gz     | $PWD/original_data/Raw_data/1450090F1381051_S4_L001_R2_001.fastq.gz     |

#### FASTQ Format Overview

FASTQ is a standard file format widely used in bioinformatics to store biological sequences and associated quality scores from high-throughput sequencing machines.

##### Structure

A FASTQ file consists of records, each representing a sequence read. Each record includes:

1. **Sequence Identifier Line (ID):**
   - Starts with '@'.
   - Uniquely identifies the sequence.

   Example:
   ```
   @SEQ_ID
   ```

2. **Sequence Line:**
   - Contains the actual nucleotide sequence (A, T, G, C, or N).

   Example:
   ```
   GATCGGAAGAGCACACGTCTGAACTCCAGTCAC
   ```

3. **Quality Identifier Line (Optional, starts with '+'):**
   - Starts with '+' and may repeat the sequence ID.

   Example:
   ```
   +
   ```

4. **Quality Scores Line:**
   - Represents quality scores for each nucleotide using ASCII characters.

   Example:
   ```
   BCCFFFFFHHHHHJJIJIJJIJJJJJJJJJJJJIJJJJJJJJJIIJJJJJJJJJJJJJJHHHFFFFFDDDDDDDDDDC
   ```

##### Example

```
@SEQ_ID
GATCGGAAGAGCACACGTCTGAACTCCAGTCAC
+
BCCFFFFFHHHHHJJIJIJJIJJJJJJJJJJJJIJJJJJJJJJIIJJJJJJJJJJJJJJHHHFFFFFDDDDDDDDDDC
```

##### Usage

FASTQ files are crucial for various bioinformatics tasks, including read mapping and variant calling. Understanding this format is essential for effective data analysis.

### 0.2) piglets Metadata
This is a small sample of the metadata provided as tsv format:
   

| sample-id              | serial   | swab_ID | Animal ID | sow | room | sex | diarrhea | neigh | is_sow | gestations | nest | alive | dead | transferred | uw_el | weaned | ppt_sow                                         |
|------------------------|----------|---------|-----------|-----|------|-----|----------|-------|--------|------------|------|-------|------|-------------|-------|--------|-------------------------------------------------|
| 1450087F1381048_S1_L001 | 1381048  | 1-A01   | S1_P0_T0  | 6247| 1    | f   | n        | 6262  | y      | 2          | 23   | 19    | 4    | 2           | 2     | 15     | Micospectone (Lincomycin/spectinomycin); Fenleve (ketoprofene) |
| 1450088F1381049_S2_L001 | 1381049  | 2-A02   | S1_P1_T0  | 6247| 1    | m   | e        | 6262  | n      | 2          | 23   | 19    | 4    | 2           | 2     | 15     | Micospectone (Lincomycin/spectinomycin); Fenleve (ketoprofene) |
| 1450089F1381050_S3_L001 | 1381050  | 3-A03   | S1_P2_T0  | 6247| 1    | f   | e        | 6262  | n      | 2          | 23   | 19    | 4    | 2           | 2     | 15     | Micospectone (Lincomycin/spectinomycin); Fenleve (ketoprofene) |
| 1450090F1381051_S4_L001 | 1381051  | 4-A04   | S1_P3_T0  | 6247| 1    | m   | e        | 6262  | n      | 2          | 23   | 19    | 4    | 2           | 2     | 15     | Micospectone (Lincomycin/spectinomycin); Fenleve (ketoprofene) |
| 1450091F1381052_S5_L001 | 1381052  | 5-A05   | S2_P0_T0  | 6261| 1    | f   | n        | 5869  | y      | 2          | 27   | 24    | 3    | 6           | 4     | 14     | none                                            |
| 1450092F1381053_S6_L001 | 1381053  | 6-A06   | S2_P1_T0  | 6261| 1    | f   | e        | 5869  | n      | 2          | 27   | 24    | 3    | 6           | 4     | 14     | none                                            |
| 1450093F1381054_S7_L001 | 1381054  | 7-A07   | S2_P2_T0  | 6261| 1    | f   | e        | 5869  | n      | 2          | 27   | 24    | 3    | 6           | 4     | 14     | none                                            |
| 1450094F1381055_S8_L001 | 1381055  | 8-A08   | S2_P3_T0  | 6261| 1    | f   | e        | 5869  | n      | 2          | 27   | 24    | 3    | 6           | 4     | 14     | none                                            |
| 1450095F1381056_S9_L001 | 1381056  | 9-A09   | S3_P0_T0  | 5982| 1    | f   | n        | 6150  | y      | 5          | 24   | 23    | 1    | 5           | 3     | 15     | none                                            |
| 1450096F1381057_S10_L001| 1381057  | 10-A10  | S3_P1_T0  | 5982| 1    | f   | e        | 6150  | n      | 5          | 24   | 23    | 1    | 5           | 3     | 15     | none                                            |
| 1450097F1381058_S11_L001| 1381058  | 11-A11  | S3_P2_T0  | 5982| 1    | m   | e        | 6150  | n      | 5          | 24   | 23    | 1    | 5           | 3     | 15     | none                                            |
| 1450098F1381059_S12_L001| 1381059  | 12-A12  | S3_P3_T0  | 5982| 1    | m   | e        | 6150  | n      | 5          | 24   | 23    | 1    | 5           | 3     | 15     | none                                            |

#### Metadata Explanations

- **sow**: [numeric] Identifies the family through the mother sow ID.

- **room**: [numeric] Families were divided into 3 rooms, conserved from birth to weaning.

- **sex**: [categorical] Gender of the animal.

- **diarrhea**: [categorical] Can be 'y' (yes), 'n' (no), or 'e' (hematic); the latter was essentially for piglets that had almost nothing inside at 24h, so the rectal walls were slightly more prone to be scratched by the swab.

- **neigh**: [numeric] Identifies the neighborhood family since water bowls from which the piglets drank were shared between 2 families.

- **is_sow**: [boolean] Dummy variable for faster identification of mothers.

- **gestations**: [numeric] Number of gestations of the sow.

- **nest**: [numeric] Number of piglets given birth (brothers for piglets).

- **alive**: [numeric] Number of survived piglets after birth.

- **dead**: [numeric] Number of dead piglets after birth.

- **transferred**: [numeric] Number of piglets transferred TO another sow.

- **uw_el**: [numeric] Number of piglets eliminated from the nest due to underweight issue.

- **weaned**: [numeric] Number of piglets survived until weaning.

- **ppt_sow**: [categorical] Treatment received by the sow post-partum.

#### Meta data considerations (Challange)

1. **Redundancy in Numeric Features**

   Certain numeric features like 'nest,' 'alive,' 'dead,' etc., may appear redundant. It's advisable to assess if any of them can be omitted without sacrificing the integrity of the analysis.

2. **Postpartum Treatments**

   Notably, only one sow underwent postpartum treatments. Considering to eliminate the column altogether.

3. **Gestation Classification**

   Gestation is currently treated as a numeric variable. However, there is potential value in dichotomizing it between primiparous and pluriparous, aligning with the classical classification employed within the farm. This classification could enhance the granularity of the analysis and provide more nuanced results.


#### Work with Metadata in qiime2

In the context of the **piglet microbiome study**, the provided metadata samples serve as a pivotal component for extracting biological insights from the processed data through QIIME 2. Within these piglet samples, the metadata encompasses crucial technical details, such as the **DNA barcodes employed in multiplexed sequencing, and specific descriptions including sow identification, room, sex, presence of diarrhea, neighborhood family identification, and gestation information**. Furthermore, the feature metadata within the samples includes annotations like the **sow's postpartum treatment category**.

For the piglet microbiome study, the initial steps involve the collection of metadata specific to the piglet samples before commencing a QIIME 2 analysis. In this case, the data provided earlier will undergo a comprehensive analysis from the beginning to assess if certain metadata can be omitted or modified.

In this context, the investigator has the flexibility to determine the information to be collected and tracked as metadata for the study. It is our opportunity to capture information deemed crucial for the piglet microbiome analyses, as QIIME 2 does not automatically gather this information from the samples. **In cases of uncertainty, it is advisable to collect comprehensive metadata for the piglet samples, considering the potential challenges of retroactively obtaining certain types of information related to piglet health and characteristics**.

[Qiime2 Metadata Details](https://docs.qiime2.org/2023.9/tutorials/metadata/)

## Starting the real analysis with qiime2

![Qiime2 pipeline](/images/overview.png)
*The edges and nodes in this overview do not represent specific actions or data types, but instead represent conceptual categories, e.g., the basic types of data or analytical goals we might have in an experiment. All of these steps and terms are discussed in more detail below.
© Copyright 2016-2022, QIIME 2 development team. Created using Sphinx 5.3.0.*

The provided data files offer insights into a standardized sequence of analyses, covering key stages up to the generation of Feature Tables, Taxonomy Classification, and the creation of Taxonomy and Phylogenetic Tree outputs. 
**Analysis Steps alrady done:**

1. **Taxonomy Classification:** Assigning taxonomic labels to sequence variants or operational taxonomic units (OTUs).

2. **Taxonomy and Phylogenetic Tree:** Constructing a hierarchical representation of taxonomic relationships and a phylogenetic tree for deeper insights.

3. **Generation of ASV, Species, and Genus Tables:**
This critical step involves creating tables for Amplicon Sequence Variants (ASVs) at the species and genus levels. ASVs offer a finer resolution, empowering researchers to investigate microbial diversity and composition in greater detail. The resulting tables provide valuable insights into the specific patterns associated with species and genera within the microbiome.

### 1) Demultiplexing 

Picture this: I've just received freshly generated FASTQ data straight from the sequencing instrument. Most next-gen sequencing instruments have the remarkable capability to analyze hundreds or even thousands of samples in a single run. How is this achieved? Through multiplexing, a technique that involves mixing a multitude of samples together.

Now, the challenge arises: how do we discern which sample each read originated from? This is where barcoding comes into play. A unique barcode (also known as an index or tag) sequence is appended to one or both ends of every sequence. Identifying and mapping these barcode sequences back to their respective samples enables us to demultiplex our sequences.

The demultiplexing process in QIIME 2 follows a workflow similar to the one outlined below:

![Demultiplexing](/images/derep-denoise.png)
*© 2021 QIIME 2 development team. Created using Sphinx 4.0.1.*

#### Demultiplexing (VIEW .qzv)

If you want to see it in interactive way you can follow the instructions [here](#installing-view-app) also i provide in an image how it should look in the terminal.
**TOFIX IMAGE**
![terminal for view app](/images/Interactive-view.png)
*when you digit any number the qzv file will open in your browser*

##### Demultiplexed Sequence Counts Summary

|                | Forward Reads | Reverse Reads |
|----------------|---------------|---------------|
| Minimum        | 45991         | 45991         |
| Median         | 71013.5       | 71013.5       |
| Mean           | 72808.958333  | 72808.958333  |
| Maximum        | 137157        | 137157        |
| Total          | 8737075       | 8737075       |

##### Demultiplexed Histogram (Forward Reads)

![Instogram demultiplexing](/images/demultiplex-summary-forward.pdf)

##### Demultiplexed Histogram (Reverse Reads)

![Instogram demultiplexing](/images/demultiplex-summary-reverse.pdf)

##### Demultiplexed Sequence Length Summary

###### Forward Reads

| Metric                  | Forwar Reads     | Reverse Reas |
|-------------------------|------------| ------------|
| Total Sequences Sampled | 10000.0    | 10000.0    |
| 2%                      | 301 nts    | 301 nts    |
| 9%                      | 301 nts    | 301 nts    |
| 25%                     | 301 nts    |  301 nts   |
| 50% (Median)            | 301 nts    | 301 nts    |
| 75%                     | 301 nts    | 301 nts    |
| 91%                     | 301 nts    | 301 nts    |
| 98%                     | 301 nts    | 301 nts    |

### 2) Demultiplexing Trimming 

#### Demultiplexing Trimming (VIEW .qzv)

##### Demultiplexed Sequence Counts Summary

| Metric   | Forward Reads | Reverse Reads |
|----------|---------------|---------------|
| Minimum  | 39756         | 39756         |
| Median   | 61078.5       | 61078.5       |
| Mean     | 62355.158333  | 62355.158333  |
| Maximum  | 107687        | 107687        |
| Total    | 7482619       | -     7482619        |

##### Demultiplexed Histogram (Forward Reads)

![Instogram demultiplexing](/images/demultiplex-summary-forward-trim.pdf)

##### Demultiplexed Histogram (Reverse Reads)

![Instogram demultiplexing](/images/demultiplex-summary-reverse-trim.pdf)

##### Demultiplexed Sequence Counts Summary

| Metric                  | Forward Reads | Reverse Reads |
|-------------------------|---------------|---------------|
| Total Sequences Sampled | 10000.0       | 10000.0       |
| 2%                      | 281 nts       | 277 nts       |
| 9%                      | 281 nts       | 277 nts       |
| 25%                     | 282 nts       | 278 nts       |
| 50% (Median)            | 283 nts       | 279 nts       |
| 75%                     | 283 nts       | 280 nts       |
| 91%                     | 284 nts       | 280 nts       |
| 98%                     | 284 nts       | 280 nts       |

### 2.2) Pre-imputation

#### Pre-imputation (VIEW .qzv)

| sample-id               | input | filtered | percentage of input passed filter | denoised | merged | percentage of input merged | non-chimeric | percentage of input non-chimeric |
|-------------------------|-------|----------|-------------------------------------|----------|--------|-----------------------------|--------------|-------------------------------------|
| 1450087F1381048_S1_L001 | 74825 | 65174    | 87.1                                | 62132    | 54583  | 72.95                       | 45234        | 60.45                               |
| 1450088F1381049_S2_L001 | 67114 | 58593    | 87.3                                | 58029    | 26867  | 40.03                       | 20511        | 30.56                               |
| 1450089F1381050_S3_L001 | 52530 | 45634    | 86.87                               | 45457    | 873    | 1.66                        | 847          | 1.61                                |
| 1450090F1381051_S4_L001 | 80751 | 70460    | 87.26                               | 69864    | 28422  | 35.2                        | 23196        | 28.73                               |
| 1450091F1381052_S5_L001 | 94343 | 83303    | 88.3                                | 80109    | 69916  | 74.11                       | 53679        | 56.9                                |

### 3) Imputation

https://genomebiology.biomedcentral.com/articles/10.1186/s13059-021-02400-4






