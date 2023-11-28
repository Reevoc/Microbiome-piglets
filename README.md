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

### Installing Docker App

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

6. Download the "data.zip" file from [Google Drive](https://drive.google.com/file/d/1B9_swa8VqM_8MaBl6xNo6z1REelOm_BY/view?usp=drive_link) and unzip it in the same directory as the Docker image:

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
