#!/bin/bash

# Define the target directory
TARGET_DIR="/home/piermarco/Documents/github/microbiome_piglets/data"

# Change the ownership to user piermarco
sudo chown -R piermarco:piermarco "$TARGET_DIR"

# Change directory permissions to 750 (rwxr-x---)
sudo find "$TARGET_DIR" -type d -exec chmod 750 {} \;

# Change file permissions to 640 (rw-r-----)
sudo find "$TARGET_DIR" -type f -exec chmod 640 {} \;

echo "Permissions have been updated for $TARGET_DIR"
