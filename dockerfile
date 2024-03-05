# Base the image on the QIIME 2 Docker image
FROM quay.io/qiime2/amplicon:2023.9

# Install base utilities and R
RUN apt-get update && \
    apt-get install -y build-essential wget zsh jq r-base r-cran-littler && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Zsh as the default shell
RUN chsh -s /usr/bin/zsh

# Install BiocManager and R packages from Bioconductor and GitHub
RUN Rscript -e 'install.packages("devtools", repos = "https://cloud.r-project.org/")' 
RUN Rscript -e 'install.packages("BiocManager", repos = "https://cloud.r-project.org/")'
RUN Rscript -e 'BiocManager::install(c("Maaslin2"))' 
RUN Rscript -e 'devtools::install_github("lichen-lab/GMPR")' 
RUN Rscript -e 'devtools::install_github("jbisanz/qiime2R")' 
RUN Rscript -e 'devtools::install_github("ruochenj/mbImpute/mbImpute R package")'

# Install Python packages
RUN pip install colorama pandas matplotlib numpy beautifulsoup4 seaborn scikit-learn rich 

# Create the microbiome folder in the Docker image
RUN mkdir -p /home/microbiome

RUN conda create --name microbiome --clone qiime2-amplicon-2023.9 && \
    conda env remove --name qiime2-amplicon-2023.9

WORKDIR /home/microbiome


# git clone
# RUN apt-get install -y git
# RUN git clone https://github.com/Reevoc/Microbiome-piglets.git


