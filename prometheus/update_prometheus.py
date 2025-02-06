#!/usr/bin/env python3

import json
import subprocess
import yaml
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the network from environment variable
network = os.getenv('NETWORK', 'default-network')  # 'default-network' is a fallback value

# Define the absolute path to prometheus.yml
PROMETHEUS_CONFIG = '/home/ubuntu/prometheus/prometheus.yml'

def clean_json(js_string):
    """
    Clean and fix JSON string issues
    """
    # Remove any console output lines that start with '>'
    lines = [line for line in js_string.split('\n') if not line.strip().startswith('>')]
    js_string = '\n'.join(lines)

    # Fix double quotes in content URLs
    js_string = re.sub(r'""https":', '"https":', js_string)

    # Fix any remaining invalid JSON syntax
    js_string = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', js_string)
    js_string = js_string.replace("'", '"')

    return js_string

def get_hosts():
    """
    Execute CLI command and extract hosts from the response
    """
    try:
        print("Executing earthfast-cli command...")
        # Updated command
        result = subprocess.run(
            f'npx earthfast-cli node list --skip=0 --json '
            f'--rpc https://eth-sepolia.g.alchemy.com/v2/TXa-YpnaYaMGNqd9ZZ0Or4lHx9wwo8AN '
            f'--network {network} --enabled',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Command failed with error: {result.stderr}")
            return []

        # Clean and parse JSON
        cleaned_json = clean_json(result.stdout)
        try:
            data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print("Raw output:", result.stdout[:200])  # Print first 200 chars for debugging
            return []

        # Extract hosts from nodes
        hosts = set()
        for node in data:
            if ('host' in node and
                not node.get('disabled', False) and
                node['host']):
                hosts.add(node['host'])

        if hosts:
            print(f"Found {len(hosts)} hosts:")
            for host in sorted(hosts):
                print(f"- {host}")
        else:
            print("No valid hosts found in the response")

        return list(hosts)

    except Exception as e:
        print(f"Error getting hosts: {e}")
        import traceback
        print(traceback.format_exc())
        return []

def update_prometheus_config():
    """
    Update prometheus.yml with new hosts
    """
    try:
        hosts = get_hosts()
        if not hosts:
            print("No hosts found to update")
            return False

        config_file = PROMETHEUS_CONFIG
        backup_file = f"{config_file}.backup"

        print(f"Reading config from: {config_file}")

        # Read current config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        # Create backup
        with open(backup_file, 'w') as f:
            yaml.dump(config, f)

        # Update targets
        for job in config['scrape_configs']:
            if job['job_name'] == 'content-nodes':
                job['static_configs'][0]['targets'] = sorted(hosts)
                print(f"Updated content-nodes targets with {len(hosts)} hosts")
                break

        # Write updated config
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        print("Successfully updated prometheus.yml")
        return True

    except Exception as e:
        print(f"Error updating config: {e}")
        if 'backup_file' in locals() and os.path.exists(backup_file):
            os.rename(backup_file, config_file)
        return False

def reload_prometheus():
    """
    Reload Prometheus configuration
    """
    try:
        print("Attempting to reload Prometheus configuration...")
        result = subprocess.run(
            ['curl', '-X', 'POST', 'http://localhost:9090/-/reload'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Prometheus configuration reloaded successfully")
            return True
        else:
            print(f"Error reloading Prometheus: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error reloading Prometheus: {e}")
        print("Full traceback:")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Starting Prometheus configuration update...")
    if update_prometheus_config():
        reload_prometheus()
    else:
        print("Failed to update Prometheus configuration")
