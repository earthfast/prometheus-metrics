#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Define the paths
PROJECT_DIR="."
PROMETHEUS_SCRIPT="$PROJECT_DIR/prometheus/update_prometheus.py"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"

# Navigate to the project directory
cd $PROJECT_DIR || exit

# Pull the latest changes from the GitHub repository
echo "Pulling latest changes from GitHub..."
ssh-add ~/.ssh/id_rsa
eval "$(ssh-agent -s)"
git pull origin main

# Activate the virtual environment
source myenv/bin/activate

# Install dependencies if not already installed
pip install pyyaml python-dotenv

# Run the update_prometheus.py script
echo "Updating Prometheus configuration..."
python3 $PROMETHEUS_SCRIPT

# Restart the Prometheus container
echo "Restarting Prometheus container..."
docker-compose -f $DOCKER_COMPOSE_FILE restart prometheus

# Deactivate the virtual environment
deactivate

echo "Process completed."
