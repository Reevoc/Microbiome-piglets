FROM bioconductor/bioconductor_docker:RELEASE_3_18

# Install base utilities
RUN apt-get update && \
    apt-get install -y build-essential wget zsh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Zsh as the default shell
RUN chsh -s /usr/bin/zsh

# Install miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O ~/miniconda.sh && \
    /usr/bin/zsh ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

# Put conda in the path so we can use conda activate
ENV PATH=/opt/conda/bin:$PATH

# Updating Miniconda and install wget
RUN conda update conda && \
    conda install wget

# Install QIIME 2
RUN wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml && \
    conda env create -n microbiome --file qiime2-amplicon-2023.9-py38-linux-conda.yml && \
    rm qiime2-amplicon-2023.9-py38-linux-conda.yml

# Install R package from Bioconductor
RUN Rscript -e 'requireNamespace("BiocManager"); BiocManager::install(c("Maaslin2", "ALDEx2"));'

# Install R packages from GitHub
RUN Rscript -e 'library(devtools); install_github("lichen-lab/GMPR");' && \
    Rscript -e 'library(devtools); install_github("jbisanz/qiime2R");' && \
    Rscript -e 'library(devtools); install_github("ruochenj/mbImpute/mbImpute R package");' && \
    Rscript -e 'install.packages("radian", repos = "https://cloud.r-project.org/")'

# Install Python packages
RUN pip install colorama pandas matplotlib numpy beautifulsoup4 seaborn scikit-learn

# Create the microbiome folder in the Docker image
RUN mkdir -p /home/microbiome
# TODO: move upper in docker file just to fast fix matrix problem of R
# Install R packages from CRAN, including Matrix
RUN install2.r --error readxl compositions Matrix
# TODO: move upper in docker file just to fast compile docker
RUN pip install rich
#  install.packages("ape")
RUN Rscript -e 'install.packages("ape", repos = "https://cloud.r-project.org/")'

