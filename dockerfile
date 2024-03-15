# Base the image on the QIIME 2 Docker image
FROM quay.io/qiime2/amplicon:2023.9

# Install base utilities, R, and sudo
RUN apt-get update && \
    apt-get install -y build-essential wget zsh jq r-base r-cran-littler sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Zsh as the default shell for root
RUN chsh -s /usr/bin/zsh

# Install BiocManager and R packages from Bioconductor and GitHub
RUN Rscript -e 'install.packages("devtools", repos = "https://cloud.r-project.org/")' 
RUN Rscript -e 'install.packages("BiocManager", repos = "https://cloud.r-project.org/")'
RUN Rscript -e 'BiocManager::install(c("Maaslin2"))' 
RUN Rscript -e 'devtools::install_github("lichen-lab/GMPR")' 
RUN Rscript -e 'devtools::install_github("jbisanz/qiime2R")' 
RUN Rscript -e 'devtools::install_github("ruochenj/mbImpute/mbImpute R package")'

# Install Python packages
RUN pip install colorama pandas matplotlib numpy beautifulsoup4 seaborn scikit-learn rich networkx

# Create a user 'microbiome', set home directory, give sudo privileges, and set default shell to zsh
RUN useradd -m -s /usr/bin/zsh microbiome && \
    echo "microbiome ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/microbiome

# Set the working directory
WORKDIR /home/microbiome/

# Switch to the 'microbiome' user
USER microbiome
