# Microbiome Piglets: A Guide to Getting Started

Welcome to the Microbiome Piglets GitHub repository! This ReadMe is designed to help you set up and run the project effectively on your local machine. Whether you're aiming for development, testing, or exploring the data, these instructions will guide you through the process.

## Initial Setup

### Essential Software

Before you start, ensure you have these tools installed:

- **Git**: [Download Git](https://git-scm.com/)
- **Docker**: [Download Docker](https://www.docker.com/)

### Cloning the Repository

1. Open your terminal and navigate to your preferred directory:

   ```bash
   cd /your-desired-path/
   ```

2. Clone the Microbiome Piglets repository:

   ```bash
   git clone https://github.com/Reevoc/Microbiome-piglets.git
   ```

### Setting Up Docker

We use a Bioconductor Docker image for this project. To set it up:

1. **Install Docker on Linux**: [Installation Guide](https://docs.docker.com/engine/install/ubuntu/). After installing, verify the installation by running:

   ```bash
   docker --help
   ```
   Or check your Docker version:
   ```bash
   docker --version
   ```

2. **Data Access**: Fill out this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeKRsjQGNdVdc4p3p-S8nd3CzaONulH37o6G3FsukSVDElz-Q/viewform) to receive the dataset links from Google Drive. You will receive two zipped files: `microbioma-starter-pack.zip` for initial setup and `microbiome-final-pack.zip` containing complete data and analyses.

   After downloading the data:
   ```bash
   cd /your-data-download-path/
   unzip data.zip
   rm data.zip
   mv /your-data-folder-path/ /path-to-cloned-repository/data
   ```

3. **Building the Docker Image**:
   
   Navigate to the directory containing the Dockerfile and build the image:
   ```bash
   cd /your-cloned-repository-path/dockerfile
   docker build -t microbiome_piglets .
   ```

4. **Running the Docker Image**:

   Launch the Docker container and attach it to the repository's folder:
   ```bash
   docker run -it -v ./:/home/microbiome microbiome_piglets /usr/bin/zsh
   ```

5. **Accessing the Docker Container**:

   Use the following commands to access your running Docker container:
   ```bash
   docker exec -it <container_id_or_name> bash 
   ```
   Find your container ID or name with:
   ```bash
   docker ps
   ```

6. **Launching the App**:

   Run the app script:
   ```bash
   cd /docker_app/
   bash app.sh
   ```

## Using the App

Our application is designed to be user-friendly and interactive. It will guide you through each step, asking for your input on the desired operations. Remember, on your first run, you'll need to set up everything as prompted. In subsequent runs, you can choose to skip certain steps and focus on specific areas as needed. Happy exploring!
