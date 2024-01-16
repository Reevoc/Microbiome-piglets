# taken from sys biology a lot of stuff already inside
FROM bioconductor/bioconductor_docker:RELEASE_3_18

# Install base utilities
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y wget && \
    apt-get install -y zsh && \    
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Zsh as the default shell
RUN chsh -s /usr/bin/zsh

# Install miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in the path so we can use conda activate
ENV PATH=/opt/conda/bin:$PATH

# Updating Miniconda and install wget
RUN conda update conda && \
    conda install wget

RUN wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml
RUN conda env create -n microbiome --file qiime2-amplicon-2023.9-py38-linux-conda.yml
RUN rm qiime2-amplicon-2023.9-py38-linux-conda.yml

# Install R package from Bioconductor
RUN Rscript -e 'requireNamespace("BiocManager"); BiocManager::install(c("Maaslin2", "ALDEx2"));'

# Install R packages from CRAN
RUN install2.r --error readxl
RUN install2.r --error compositions  # Add this line to install the compositions package

# Install R packages from GitHub
RUN Rscript -e 'library(devtools); install_github("lichen-lab/GMPR");'
RUN Rscript -e 'library(devtools); install_github("jbisanz/qiime2R");'
RUN Rscript -e 'library(devtools); install_github("ruochenj/mbImpute/mbImpute R package");'
# RUN Rscript -e 'library(devtools); install_github("stefpeschel/NetCoMi", dependencies = c("Depends", "Imports", "LinkingTo"), repos = c("https://cloud.r-project.org/",BiocManager::repositories()));'
RUN Rscript -e 'install.packages("radian", repos = "https://cloud.r-project.org/")'

# install python packages
RUN pip install colorama
RUN pip install pandas
RUN pip install matplotlib
RUN pip install numpy
RUN pip install beautifulsoup4
RUN pip install seaborn
RUN pip install scikit-learn
# Create the microbiome folder in the Docker image
RUN mkdir -p /home/microbiome