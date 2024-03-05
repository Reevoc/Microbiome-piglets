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
   cd /your-path-to-repository/
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

2. Download the "data.zip" file from [Google Drive](https://drive.google.com/file/d/1Kx87HDn-XSEu_YU5cFvs7jH2YGkJLU-w/view?usp=drive_xclink) and unzip it in the same directory as the Docker image(mv just move the data downloaded to the download directory to the docker_app folder that is palced in the git repository):

   ```bash
   cd /path-to-your-download-where-data.zip/
   unzip data.zip
   rm data.zip
   mv path-to-your-download-where-data-folder/ path-to-your-downloaded-git-repository/data
   ```

3. Build the Docker image (ensure you are in the correct directory before building, the correct folder is the folder where the Dockerfile is located):

   ```bash
   cd path-to-your-downloaded_git_repository/dockerfile
   docker build -t microbiome_piglets .
   ```

4. Run the Docker image and attach the folder from the git repository to the Docker container (./ stay for the current directory it should be the same as git folder):

   ```bash
   # docker run -e PASSWORD=pass -p 8787:8787 -d -v ./:/home/microbiome microbiome_piglets
   # version below to check if stable
   docker run -e PASSWORD=pass -p 8787:8787 -d -v $(pwd):/home/microbiome -u $(id -u):$(id -g) microbiome_piglets
   docker run -it -u $(id -u):$(id -g) -v "$(pwd)":/home/microbiome microbiome_piglets /bin/bash


   ```

5. Run the Docker image:

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
   source ./view_app.sh
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

### Methods and Visualizers
QIIME 2 plugins define methods and visualizers for conducting analyses. Methods accept artifacts and parameters as input, producing one or more artifacts as output. Visualizers, on the other hand, produce a single visualization as terminal output. These components form the building blocks of QIIME 2 analyses, offering flexibility and customization.
The web site if the view app dose not work is [Qiime2 View](https://view.qiime2.org/)

*© Copyright 2016-2022, QIIME 2 development team. Created using Sphinx 5.3.0.*

