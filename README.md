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
   cd /path-to-your-downloaded_git_repository/dockerfile
   docker build -t microbiome_piglets .
   ```

4. Run the Docker image and attach the folder from the git repository to the Docker container (./ stay for the current directory it should be the same as git folder):

   ```bash
   docker run -it -v ./:/home/microbiome microbiome_piglets /usr/bin/zsh
   ```

5. Run the Docker image:
   ```bash
   docker exec -it <container_id_or_name> /bin/bash
   ```

   - Replace `<container_id_or_name>` with the ID or name of the Docker container, which you can find using:
      ```bash
      docker ps
      ```
6. Run the app:
```bash
   cd /docker_app/
   bash app.sh
```
