#!/usr/bin/env python3
import subprocess
import re

# Configuration
NETWORK_PREFIX = "192.168.1."  # Edit this to match your network

def get_container_ip(container_id):
    """Get IP address for a container using lxc-info"""
    try:
        result = subprocess.run(['lxc-info', '-n', str(container_id)], 
                              capture_output=True, text=True)
        
        # Look for IP line in output
        for line in result.stdout.split('\n'):
            if 'IP:' in line:
                ip = line.split('IP:')[1].strip()
                # Only return IP if it's in our network
                if ip.startswith(NETWORK_PREFIX):
                    return ip
                else:
                    print(f"Skipping IP {ip} as it's not in network {NETWORK_PREFIX}0/24")
    except Exception as e:
        print(f"Error getting IP for container {container_id}: {e}")
    return None

def update_container_tags(container_id, ip):
    """Update container tags with IP address"""
    try:
        # Get current tags
        result = subprocess.run(['pct', 'config', str(container_id)], 
                              capture_output=True, text=True)
        
        # Parse current tags
        tags = []
        for line in result.stdout.split('\n'):
            if line.startswith('tags:'):
                current_tags = line.split('tags: ')[1].strip()
                tags = [tag for tag in current_tags.split(',') if tag and not tag.startswith('ip-')]
        
        # Add IP tag
        if ip:
            tags.append(f'ip-{ip.replace(".", "-")}')
        
        # Update tags
        tag_string = ','.join(tags)
        subprocess.run(['pct', 'set', str(container_id), '--tags', tag_string])
        print(f"Updated container {container_id} with tags: {tag_string}")
        
    except Exception as e:
        print(f"Error updating tags for container {container_id}: {e}")

def main():
    print(f"Looking for IPs in network: {NETWORK_PREFIX}0/24")
    
    # Get list of containers
    try:
        result = subprocess.run(['pct', 'list'], capture_output=True, text=True)
        
        # Parse container IDs
        container_ids = []
        for line in result.stdout.split('\n')[1:]:  # Skip header line
            if line.strip():
                container_id = line.split()[0]
                container_ids.append(container_id)
        
        # Update each container
        for container_id in container_ids:
            print(f"\nProcessing container {container_id}")
            ip = get_container_ip(container_id)
            if ip:
                print(f"Found IP: {ip}")
                update_container_tags(container_id, ip)
            else:
                print(f"No matching IP found for container {container_id}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
