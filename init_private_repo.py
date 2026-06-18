#!/usr/bin/env python3
"""
Initialize Private Repository Structure for Telemetry
======================================================

This script creates the telemetry directory structure in your private
"shah" repository and initializes the required JSON files.

Usage:
  python3 init_private_repo.py

Environment Variables:
  GITHUB_TELEMETRY_TOKEN - Your GitHub PAT token
  TELEMETRY_REPO_OWNER - Repository owner (default: shah786628)
  TELEMETRY_REPO_NAME - Repository name (default: shah)
"""

import os
import sys
import json
import base64
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: requests library required: pip install requests")
    sys.exit(1)


def init_private_repo():
    """Initialize telemetry structure in private GitHub repository."""
    
    # Get configuration
    token = os.environ.get("GITHUB_TELEMETRY_TOKEN")
    if not token:
        print("ERROR: GITHUB_TELEMETRY_TOKEN environment variable not set")
        print("Create a GitHub PAT at: https://github.com/settings/tokens")
        sys.exit(1)
    
    repo_owner = os.environ.get("TELEMETRY_REPO_OWNER", "shah786628")
    repo_name = os.environ.get("TELEMETRY_REPO_NAME", "shah")
    branch = os.environ.get("TELEMETRY_REPO_BRANCH", "main")
    
    print(f"Initializing telemetry structure in: {repo_owner}/{repo_name}")
    print(f"Branch: {branch}")
    print()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "nawaz1-telemetry-init"
    }
    
    # Files to create
    files_to_create = {
        "telemetry/machines.json": {
            "machines": [],
            "total_machines": 0,
            "active_machines": 0,
            "revoked_machines": 0
        },
        "telemetry/auto_kill_incidents.json": {
            "incidents": [],
            "total_incidents": 0,
            "critical_incidents": 0,
            "pending_review": 0
        },
        "telemetry/analytics/.gitkeep": "",
        "kill_switch/revoked_tags.json": {
            "revoked_tags": [],
            "total_revoked": 0
        },
        "kill_switch/global_kill.txt": "INACTIVE",
        "kill_switch/auto_killed_binaries.json": {
            "binaries": [],
            "total_auto_killed": 0
        }
    }
    
    success_count = 0
    
    for file_path, content in files_to_create.items():
        print(f"Creating: {file_path}...")
        
        # Encode content
        if isinstance(content, dict):
            encoded_content = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
        else:
            encoded_content = base64.b64encode(content.encode()).decode()
        
        # Create file via GitHub API
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        
        payload = {
            "message": f"Initialize {file_path}",
            "content": encoded_content,
            "branch": branch
        }
        
        try:
            resp = requests.put(url, headers=headers, json=payload, timeout=10)
            
            if resp.status_code in (200, 201):
                print(f"  ✓ Created successfully")
                success_count += 1
            elif resp.status_code == 422:
                print(f"  ⚠ File already exists (skipping)")
                success_count += 1
            else:
                print(f"  ✗ Failed: {resp.status_code}")
                print(f"    {resp.text[:200]}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    print("="*80)
    print(f"Initialization complete: {success_count}/{len(files_to_create)} files created")
    print("="*80)
    
    if success_count == len(files_to_create):
        print("\n✓ Private repository structure initialized successfully!")
        print("\nNext steps:")
        print("  1. Build new binaries with telemetry:")
        print("     cd nawaz1_dev")
        print("     cargo build --release --target x86_64-unknown-linux-gnu")
        print()
        print("  2. Test telemetry:")
        print("     ./target/x86_64-unknown-linux-gnu/release/nawaz1-server")
        print()
        print("  3. View registered machines:")
        print("     python3 telemetry_dashboard.py --list-machines")
        return 0
    else:
        print("\n✗ Some files failed to create. Check errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(init_private_repo())
