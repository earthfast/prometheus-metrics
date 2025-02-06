# Prometheus Node Monitoring

This project sets up a Prometheus monitoring system to dynamically fetch and update the list of nodes. It includes a Python script to automate the process of updating the Prometheus configuration with the latest node information.

## Features

- **Dynamic Node Fetching**: A Python script (`update_prometheus.py`) fetches the list of nodes using the EarthFast CLI and updates the Prometheus configuration.
- **Automated Configuration Update**: The script updates the `prometheus.yml` file with the latest node targets and reloads the Prometheus configuration without requiring a restart.
- **Backup and Restore**: Before updating, the script creates a backup of the existing Prometheus configuration.
- **Scheduled Updates**: A cron job is set up to run the update script daily at 3 AM.

## Setup and Installation

### Prerequisites

- **Node.js and npm**: Required to run the EarthFast CLI.
- **Python 3**: To execute the update script.
- **Docker and Docker Compose**: To manage the Prometheus and related services.

### Installation Steps

1. **Install Node.js and npm**:
   ```bash
   sudo apt update
   sudo apt install nodejs npm
   ```

2. **Set up the Python environment**:
   Ensure Python 3 is installed on your system.

3. **Clone the repository**:
   ```bash
   git clone git@github.com:earthfast/prometheus-metrics.git
   cd prometheus-metrics
   ```

4. **Install Python dependencies**:
   If there are any Python dependencies, install them using pip.

5. **Set up the cron job**:
   Add the following line to your crontab to schedule the script:
   ```bash
   0 3 * * * /usr/bin/python3 /home/ubuntu/prometheus/update_prometheus.py >> /home/ubuntu/update_prometheus.log 2>&1
   ```

6. **Start the Docker services**:
   ```bash
   docker-compose up -d
   ```

## Usage

- **Manual Execution**: You can manually run the update script to test its functionality:
  ```bash
  /home/ubuntu/prometheus/update_prometheus.py
  ```

- **Verify Prometheus Targets**: After running the script, verify the updated nodes at:
  [Prometheus Targets](https://prometheus.earthfast.com/targets)

- **Restart Prometheus**: If needed, restart the Prometheus container:
  ```bash
  docker-compose restart prometheus
  ```

## Code Overview

- **Prometheus Configuration**: The configuration file is located at `prometheus/prometheus.yml`.
- **Update Script**: The script responsible for updating the configuration is `update_prometheus.py`.
- **Docker Setup**: The Docker setup is defined in `docker-compose.yml`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
