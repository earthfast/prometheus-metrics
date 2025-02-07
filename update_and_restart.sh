#!/bin/bash

# Define the paths
PROJECT_DIR="."
PROMETHEUS_SCRIPT="$PROJECT_DIR/prometheus/update_prometheus.py"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"

# Function to check the exit status of the last command
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error in step: $1"
        exit 1
    fi
}

# Navigate to the project directory
cd $PROJECT_DIR || exit

# Pull the latest changes from the GitHub repository
echo "Pulling latest changes from GitHub..."
ssh-add ~/.ssh/id_rsa
eval "$(ssh-agent -s)"
git pull origin main
check_status "git pull"

# Activate the virtual environment
source myenv/bin/activate

# Install dependencies if not already installed
pip install pyyaml python-dotenv

# Run the update_prometheus.py script
echo "Updating Prometheus configuration..."
python3 $PROMETHEUS_SCRIPT
check_status "update_prometheus.py"

# Restart the Prometheus container
echo "Restarting Prometheus container..."
docker-compose -f $DOCKER_COMPOSE_FILE restart prometheus
check_status "docker-compose restart"

# Deactivate the virtual environment
deactivate

echo "Process completed."
