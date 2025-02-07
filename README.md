# EarthFast Nodes Monitoring with Prometheus and Grafana

This project sets up a comprehensive monitoring system using Prometheus and Grafana to visualize and manage the nodes created for the EarthFast network. The system is designed to dynamically fetch and update the list of nodes, ensuring that the monitoring data is always up-to-date.

## Features

- **Prometheus Monitoring**: Collects metrics from EarthFast nodes and other services.
- **Grafana Dashboard**: Provides a visual interface to monitor node performance and other metrics.
- **Dynamic Node Fetching**: A Python script (`update_prometheus.py`) fetches the list of nodes using the EarthFast CLI and updates the Prometheus configuration.
- **Automated Configuration Update**: The script updates the `prometheus.yml` file with the latest node targets and reloads the Prometheus configuration without requiring a restart.
- **Backup and Restore**: Before updating, the script creates a backup of the existing Prometheus configuration.
- **Scheduled Updates**: A cron job is set up to run the update script daily at 3 AM.

## Setup and Installation

### Prerequisites

- **Node.js and npm**: Required to run the EarthFast CLI.
- **Python 3**: To execute the update script.
- **Docker and Docker Compose**: To manage the Prometheus and related services.

### Running the Project Locally

1. **Copy Configuration Files**:
   - Create a copy of `prometheus/prometheus.yml.example` and name it `prometheus/prometheus.yml`.
   - Create a `.env` file based on `.env.example`. Set the `NETWORK` variable to either `testnet-sepolia-staging` or `testnet-sepolia` depending on your environment.

2. **Start Docker Services**:
   - Run the following command to start the Docker container:
     ```bash
     docker compose up
     ```
   - Access the Prometheus dashboard at `http://localhost:9090` and view the targets at `http://localhost:9090/targets`.
   - Access the Grafana dashboard at `http://localhost:3000`, specifically the content node overview dashboard at `http://localhost:3000/d/content-node-overview/content-node-overview?var-timerange=7d&orgId=1&from=now-5m&to=now&timezone=browser&var-instance=$__all`.

### Updating Grafana Dashboards and Prometheus Nodes

1. **Update Grafana Dashboards**:
   - Modify the `grafana/dashboards/content-node.json` file to update the Grafana dashboard configurations.

2. **Update Prometheus Nodes**:
   - Ensure that the `prometheus.yml` file has been created from the `prometheus/prometheus.yml.example` before using the `update_prometheus.py` script to update the nodes in the `prometheus.yml` file.
   - **Install Required Dependencies**:
     - Create a virtual environment:
       ```bash
       python3 -m venv venv
       ```
     - Activate the virtual environment:
       ```bash
       source venv/bin/activate
       ```
     - Install the necessary Python dependencies:
       ```bash
       pip install pyyaml
       pip install python-dotenv
       ```
   - Run the update script:
     ```bash
     python3 prometheus/update_prometheus.py
     ```
   - To verify that the script is correctly adding updated nodes, follow these steps:
     1. Ensure the `prometheus.yml` file is backed up automatically by the script.
     2. Run the script using the command above.
     3. Check the `prometheus.yml` file to confirm that the `content-nodes` targets have been updated with the new hosts.

3. **Verify Changes Locally**:
   - If the container is already running, restart it to apply changes:
     ```bash
     docker-compose restart
     ```
   - If the container is not running, follow step 2 of "Running the Project Locally" again to ensure everything is set up correctly.
   - Access the Prometheus dashboard at `http://localhost:9090` to verify the changes.

4. **Commit and Push Changes**:
   - Create a new branch and commit your changes.
   - Push the branch and create a Pull Request (PR) for team review.

5. **Deploy Changes to AWS Instances**:
   - Ensure you have the necessary SSH keys (`content-staging.pem` and `content-testnet.pem`) in your `.ssh` directory.
   - Update your SSH config file with the following:

     For Staging:
     ````
     Host earthfast-metrics-staging
       ForwardAgent yes
       HostName 18.116.118.113
       User ubuntu
       IdentityFile ~/.ssh/content-staging.pem
     ````

     For Testnet:
     ````
     Host earthfast-metrics-testnet
       ForwardAgent yes
       HostName 18.222.2.178
       User ubuntu
       IdentityFile ~/.ssh/content-testnet.pem
     ````

   - Connect to the instances using:
     - For Staging:
       ```bash
       ssh earthfast-metrics-staging
       ```
     - For Testnet:
       ```bash
       ssh earthfast-metrics-testnet
       ```

   - Execute the `./update_and_restart.sh` command on the instance. This command will perform the following actions:
     1. Synchronize the local codebase with the latest changes from GitHub.
     2. Run the `update_prometheus.py` script to update the Prometheus configuration with the latest node information.
     3. Restart the Docker container to apply the updates.

6. **Verify Changes on Production**:
   - Check the updated targets and dashboards at:
     - [Prometheus Targets](https://prometheus.earthfast.com/targets)
     - [Prometheus Staging Targets](https://prometheus-staging.earthfast.com/targets)
     - [Grafana Staging Dashboard](https://monitoring-staging.earthfast.com/d/content-node-overview/content-node-overview?var-timerange=7d&orgId=1&from=now-5m&to=now&timezone=browser&var-instance=$__all)
     - [Grafana Dashboard](https://monitoring.earthfast.com/d/content-node-overview/content-node-overview?var-timerange=7d&orgId=1&from=now-5m&to=now&timezone=browser&var-instance=$__all)
