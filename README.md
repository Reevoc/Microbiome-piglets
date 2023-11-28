*# Project Name

Brief description of your project.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
- [Docker](https://www.docker.com/)

### Clone the repository

1. Move to a repository where you want to download the project:

  ```bash
    cd /your/path/to/repository
  ```

2. Clone the repository:

  ```bash
    git clone https://github.com/Reevoc/Microbiome_piglets.git
  ```

### Installing Docker app

A step-by-step guide on how to set up the docker environment.
1. [Install Docker Linux Distro Ubunto](https://docs.docker.com/engine/install/ubuntu/)
   - to check if the installation is correct:
      ```bash
      docker --help
      ```
   - or to check the version:
      ```bash
      docker --version
      ```
2. Build the docker image (the dot stends for the current directory so carefully move to the correct directory before the build):

    ```bash
    docker build -t microbiome_piglets .
    ```

3. Run the docker image:

    ```bash
    docker run -e PASSWORD=pass -p 8787:8787 -d microbiome_piglets
    ```

4. Clone the usefull github repositery that we have downloaded in local in the docker image:
    
    ```bash
    docker cp /your/path/to/Microbiome_piglets/docker_app/ ID_CONTAINER:/home/microbiome
    ```
    * ID_CONTAINER is the id of the docker container that you can find with the command:
    
    ```bash
    docker ps
    ```
    
5. Change into the project directory:

    ```bash
    cd /your/path/to/Microbiome_piglets/docker_app
    ```
    

6. Go to [google drive](https://drive.google.com/file/d/1B9_swa8VqM_8MaBl6xNo6z1REelOm_BY/view?usp=drive_link) and download the file "data.zip" and unzip it in the same directory as the docker image:
  
      ```bash
      cd path/to/your/download_where_data.zip
      unzip data.zip
      rm data.zip
      ```
7. Copy the data inside the docker image
  
      ```bash
      docker cp /your/path/to/Microbiome_piglets/docker_app/data/ ID_CONTAINER:/home/microbiome
      ```
       * ID_CONTAINER is the id of the docker container that you can find with the command:
    
    ```bash
    docker ps
    ```
8. Run the docker image:
  
      ```bash
      docker exec -it <container_id_or_name> /bin/bash

      ```
       * <container_id_or_name> is the id of the docker container that you can find with the command:
    
    ```bash
    docker ps
    ```

### Installing View app

A step-by-step guide on how to set up the view environment.

1. Change into the project directory:

    ```bash
    cd /your/path/to/Microbiome_piglets
    ```

2. Install conda:
  
      ```bash
      conda install -c conda-forge mamba
      ```
3. Create the conda environment:
  
      ```bash
      wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml
      conda env create -n qiime2-amplicon-2023.9 --file qiime2-amplicon-2023.9-py38-linux-conda.yml
      rm qiime2-amplicon-2023.9-py38-linux-conda.yml
      ```
4. Activate the conda environment only need for local view on your computer:
  
      ```bash
      conda activate qiime2-amplicon-2023.9
      ```
5. Using view script to see the result:
  
      ```bash
      cd Microbiome_piglets/view
      bash view_app.sh
      ```
*