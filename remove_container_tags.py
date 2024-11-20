#!/usr/bin/env python3
import subprocess

def remove_container_tags(container_id):
    """Remove all tags from a container"""
    try:
        print(f"Removing tags from container {container_id}")
        subprocess.run(['pct', 'set', str(container_id), '--tags', ''])
        print(f"Successfully removed tags from container {container_id}")
    except Exception as e:
        print(f"Error removing tags from container {container_id}: {e}")

def main():
    # Get list of containers
    try:
        print("Getting list of containers...")
        result = subprocess.run(['pct', 'list'], capture_output=True, text=True)
        
        # Parse container IDs
        container_ids = []
        for line in result.stdout.split('\n')[1:]:  # Skip header line
            if line.strip():
                container_id = line.split()[0]
                container_ids.append(container_id)
        
        print(f"Found {len(container_ids)} containers")
        
        # Remove tags from each container
        for container_id in container_ids:
            remove_container_tags(container_id)
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
