#!/usr/bin/env python3
"""
Nawaz1 Quantum Software - Owner Telemetry & Kill-Switch Dashboard
================================================================

Private management tool for Shahnawaz Alam (owner) to:
- View all machines running nawaz1-server
- Review auto-kill incidents (RE attacks)
- Manage per-tag revocations (reversible)
- Activate global kill-switch (permanent)
- Export telemetry analytics

Repository: Your private "shah" repository (RE security data)
  - Set via environment variables: TELEMETRY_REPO_OWNER, TELEMETRY_REPO_NAME
  - Default: shah786628/shah

Public repository (nawaz1-quantum-software) is used ONLY for binary distribution.
"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required: pip install requests")
    sys.exit(1)


# ── Configuration ────────────────────────────────────────────────────────────
# Private repository for RE security & telemetry (your existing "shah" repo)
# Set via environment variables:
#   TELEMETRY_REPO_OWNER=shah786628
#   TELEMETRY_REPO_NAME=shah
#   TELEMETRY_REPO_BRANCH=main

GITHUB_REPO_OWNER = os.environ.get("TELEMETRY_REPO_OWNER", "shah786628")
GITHUB_REPO_NAME = os.environ.get("TELEMETRY_REPO_NAME", "shah")
GITHUB_REPO = f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}"

# File paths in private repo
TELEMETRY_MACHINES = "telemetry/machines.json"
AUTO_KILL_INCIDENTS = "telemetry/auto_kill_incidents.json"
REVOKED_TAGS = "kill_switch/revoked_tags.json"
GLOBAL_KILL_FILE = "kill_switch/global_kill.txt"


class TelemetryDashboard:
    """Owner dashboard for managing telemetry and kill-switches."""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "nawaz1-telemetry-dashboard"
        }
    
    # ── GitHub API Helpers ───────────────────────────────────────────────────
    def _get_file(self, path: str) -> Optional[Dict]:
        """Fetch JSON file from private GitHub repo."""
        url = f"{GITHUB_API}/contents/{path}"
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                content = base64.b64decode(data["content"]).decode("utf-8")
                return json.loads(content)
            elif resp.status_code == 404:
                return None
            else:
                print(f"ERROR: GitHub API returned {resp.status_code}")
                print(resp.text)
                return None
        except Exception as e:
            print(f"ERROR: Failed to fetch {path}: {e}")
            return None
    
    def _update_file(self, path: str, content: Dict, message: str) -> bool:
        """Update JSON file in private GitHub repo."""
        url = f"{GITHUB_API}/contents/{path}"
        
        # Get current file SHA (required for update)
        sha = None
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                sha = resp.json()["sha"]
        except:
            pass
        
        # Encode content
        encoded = base64.b64encode(json.dumps(content, indent=2).encode()).decode()
        
        # Update or create
        payload = {
            "message": message,
            "content": encoded,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha
        
        try:
            resp = requests.put(url, headers=self.headers, json=payload, timeout=10)
            return resp.status_code in (200, 201)
        except Exception as e:
            print(f"ERROR: Failed to update {path}: {e}")
            return False
    
    # ── Telemetry Functions ──────────────────────────────────────────────────
    def list_machines(self):
        """Display all registered machines."""
        print("\n" + "="*80)
        print("  REGISTERED MACHINES")
        print("="*80 + "\n")
        
        data = self._get_file(TELEMETRY_MACHINES)
        if not data:
            print("No machines registered yet.")
            return
        
        machines = data.get("machines", [])
        
        print(f"{'Tag':<20} {'Location':<25} {'First Run':<20} {'Status':<15}")
        print("-"*80)
        
        active = 0
        revoked = 0
        
        for m in machines:
            tag = m["tag"][:16] + "..."
            location = f"{m['location']['city']}, {m['location']['country']}"
            first_run = m["first_run"][:16]
            status = m.get("status", "active")
            
            status_icon = "✅" if status == "active" else "❌"
            print(f"{tag:<20} {location:<25} {first_run:<20} {status_icon} {status}")
            
            if status == "active":
                active += 1
            else:
                revoked += 1
        
        print("\n" + "="*80)
        print(f"Total: {len(machines)} | Active: {active} | Revoked: {revoked}")
        print("="*80 + "\n")
    
    def export_machines(self, output_file: str):
        """Export machine telemetry to local JSON file."""
        data = self._get_file(TELEMETRY_MACHINES)
        if data:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Exported to {output_file}")
        else:
            print("ERROR: No data to export")
    
    # ── Incident Review Functions ────────────────────────────────────────────
    def review_incidents(self):
        """Display auto-kill incidents for owner review."""
        print("\n" + "="*80)
        print("  AUTO-KILL INCIDENT REVIEW")
        print("="*80 + "\n")
        
        data = self._get_file(AUTO_KILL_INCIDENTS)
        if not data:
            print("No incidents logged yet.")
            return
        
        incidents = data.get("incidents", [])
        pending = [i for i in incidents if not i.get("owner_review", {}).get("reviewed")]
        
        if not pending:
            print("✅ No pending incidents to review")
            return
        
        print(f"⚠️  {len(pending)} incident(s) pending review:\n")
        
        for i, incident in enumerate(pending, 1):
            print(f"Incident #{i}:")
            print(f"  Machine Tag:    {incident['machine_tag']}")
            print(f"  Trigger:        {incident['trigger_reason']}")
            print(f"  Location:       {incident['location']['city']}, {incident['location']['country']}")
            print(f"  Timestamp:      {incident['timestamp']}")
            print(f"  Severity:       {incident['severity']}")
            print(f"  Attack Signs:")
            indicators = incident.get("attack_indicators", {})
            print(f"    - Debugger:   {'✅' if indicators.get('debugger_detected') else '❌'}")
            print(f"    - Tampering:  {'✅' if indicators.get('memory_tampering') else '❌'}")
            print(f"    - Modified:   {'✅' if indicators.get('binary_modified') else '❌'}")
            print()
            
            # Owner action
            action = input("Action [r=review, i=ignore, b=block-tag, s=skip]: ").strip().lower()
            
            if action == 'r':
                self._mark_reviewed(incident['machine_tag'], "Reviewed - no action")
            elif action == 'i':
                self._mark_reviewed(incident['machine_tag'], "Ignored - false positive")
            elif action == 'b':
                self.revoke_tag(incident['machine_tag'], "Owner blocked after auto-kill review")
            elif action == 's':
                continue
            
            print()
    
    def _mark_reviewed(self, tag: str, action: str):
        """Mark incident as reviewed."""
        data = self._get_file(AUTO_KILL_INCIDENTS)
        if not data:
            return
        
        for incident in data.get("incidents", []):
            if incident["machine_tag"] == tag:
                incident["owner_review"] = {
                    "reviewed": True,
                    "reviewed_by": "Shahnawaz Alam",
                    "review_timestamp": datetime.utcnow().isoformat() + "Z",
                    "action_taken": action
                }
                break
        
        if self._update_file(AUTO_KILL_INCIDENTS, data, f"Review incident: {tag[:8]}"):
            print(f"✅ Marked {tag[:8]}... as reviewed: {action}")
    
    # ── Kill-Switch Functions ────────────────────────────────────────────────
    def revoke_tag(self, tag: str, reason: str):
        """Per-tag revocation (reversible by owner)."""
        data = self._get_file(REVOKED_TAGS)
        if not data:
            data = {"revoked_tags": [], "total_revoked": 0}
        
        # Check if already revoked
        for rt in data["revoked_tags"]:
            if rt["tag"] == tag:
                print(f"⚠️  Tag {tag[:8]}... already revoked")
                return
        
        # Add revocation
        data["revoked_tags"].append({
            "tag": tag,
            "reason": reason,
            "revoked_by": "Shahnawaz Alam",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "reversible": True
        })
        data["total_revoked"] = len(data["revoked_tags"])
        
        if self._update_file(REVOKED_TAGS, data, f"Revoke tag: {tag[:8]}..."):
            print(f"❌ Tag {tag[:8]}... revoked: {reason}")
    
    def unrevoke_tag(self, tag: str, reason: str):
        """Un-revoke a tag (restore access)."""
        data = self._get_file(REVOKED_TAGS)
        if not data:
            print("No revoked tags found")
            return
        
        # Remove revocation
        data["revoked_tags"] = [rt for rt in data["revoked_tags"] if rt["tag"] != tag]
        data["total_revoked"] = len(data["revoked_tags"])
        
        if self._update_file(REVOKED_TAGS, data, f"Un-revoke tag: {tag[:8]}..."):
            print(f"✅ Tag {tag[:8]}... un-revoked: {reason}")
    
    def list_revoked_tags(self):
        """List all revoked tags."""
        print("\n" + "="*80)
        print("  REVOKED TAGS")
        print("="*80 + "\n")
        
        data = self._get_file(REVOKED_TAGS)
        if not data:
            print("No revoked tags.")
            return
        
        revoked = data.get("revoked_tags", [])
        
        print(f"{'Tag':<20} {'Reason':<40} {'Timestamp':<20}")
        print("-"*80)
        
        for rt in revoked:
            tag = rt["tag"][:16] + "..."
            reason = rt["reason"][:37] + "..."
            timestamp = rt["timestamp"][:16]
            print(f"{tag:<20} {reason:<40} {timestamp:<20}")
        
        print(f"\nTotal revoked: {len(revoked)}\n")
    
    def activate_global_kill(self, reason: str):
        """Activate global kill-switch (PERMANENT, NO RECOVERY)."""
        print("\n" + "="*80)
        print("  ⚠️  WARNING: GLOBAL KILL-SWITCH ACTIVATION")
        print("="*80)
        print(f"\n  Reason: {reason}")
        print("\n  This will PERMANENTLY revoke ALL machines")
        print("  This action CANNOT be undone")
        print("  You must generate a FRESH binary to recover")
        print("\n" + "="*80 + "\n")
        
        confirm = input("Type 'REVOKE_ALL' to confirm: ").strip()
        
        if confirm != "REVOKE_ALL":
            print("❌ Global kill-switch NOT activated")
            return
        
        content = {
            "status": "ACTIVE",
            "reason": reason,
            "activated_by": "Shahnawaz Alam",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "permanent": True
        }
        
        if self._update_file(GLOBAL_KILL_FILE, content, "GLOBAL KILL-SWITCH: REVOKE_ALL"):
            print("✅ Global kill-switch activated. All binaries suspended.")
            print("⚠️  Generate fresh binary from source to recover.")
    
    def check_global_kill(self):
        """Check if global kill-switch is active."""
        data = self._get_file(GLOBAL_KILL_FILE)
        if data and data.get("status") == "ACTIVE":
            print("\n" + "="*80)
            print("  ⚠️  GLOBAL KILL-SWITCH IS ACTIVE")
            print("="*80)
            print(f"  Reason:     {data.get('reason')}")
            print(f"  Activated:  {data.get('timestamp')}")
            print(f"  Activated By: {data.get('activated_by')}")
            print(f"  Permanent:  {data.get('permanent')}")
            print("\n  ALL MACHINES ARE PERMANENTLY REVOKED")
            print("  Generate fresh binary from source to recover")
            print("="*80 + "\n")
            return True
        else:
            print("✅ Global kill-switch is INACTIVE")
            return False
    
    # ── Analytics Functions ──────────────────────────────────────────────────
    def show_analytics(self):
        """Display telemetry analytics."""
        print("\n" + "="*80)
        print("  TELEMETRY ANALYTICS")
        print("="*80 + "\n")
        
        # Machine analytics
        machines_data = self._get_file(TELEMETRY_MACHINES)
        if machines_data:
            machines = machines_data.get("machines", [])
            
            # Count by country
            countries = {}
            for m in machines:
                country = m["location"]["country"]
                countries[country] = countries.get(country, 0) + 1
            
            print("Machines by Country:")
            for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
                print(f"  {country:<30} {count} machines")
            
            # Count by OS
            os_counts = {}
            for m in machines:
                os_name = m["os"].split()[0]  # e.g., "Ubuntu", "Debian"
                os_counts[os_name] = os_counts.get(os_name, 0) + 1
            
            print("\nMachines by OS:")
            for os_name, count in sorted(os_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {os_name:<30} {count} machines")
        
        # Incident analytics
        incidents_data = self._get_file(AUTO_KILL_INCIDENTS)
        if incidents_data:
            incidents = incidents_data.get("incidents", [])
            
            print(f"\nAuto-Kill Incidents:")
            print(f"  Total incidents:    {len(incidents)}")
            
            pending = [i for i in incidents if not i.get("owner_review", {}).get("reviewed")]
            print(f"  Pending review:     {len(pending)}")
            
            # Count by trigger type
            triggers = {}
            for i in incidents:
                trigger = i["trigger_reason"].split()[0]  # e.g., "Debugger", "Memory"
                triggers[trigger] = triggers.get(trigger, 0) + 1
            
            print("\n  Incidents by Trigger:")
            for trigger, count in sorted(triggers.items(), key=lambda x: x[1], reverse=True):
                print(f"    {trigger:<28} {count} incidents")
        
        print("\n" + "="*80 + "\n")


# ── Command Line Interface ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Nawaz1 Telemetry & Kill-Switch Dashboard")
    parser.add_argument("--token", type=str, help="GitHub PAT token (or set GITHUB_TELEMETRY_TOKEN env)")
    
    # Commands
    parser.add_argument("--list-machines", action="store_true", help="List all registered machines")
    parser.add_argument("--export-machines", type=str, help="Export machines to JSON file")
    parser.add_argument("--review-incidents", action="store_true", help="Review auto-kill incidents")
    parser.add_argument("--list-revoked", action="store_true", help="List revoked tags")
    parser.add_argument("--revoke-tag", type=str, help="Revoke specific machine tag")
    parser.add_argument("--unrevoke-tag", type=str, help="Un-revoke specific machine tag")
    parser.add_argument("--reason", type=str, default="Owner action", help="Reason for action")
    parser.add_argument("--global-kill", action="store_true", help="Activate global kill-switch")
    parser.add_argument("--check-global", action="store_true", help="Check global kill-switch status")
    parser.add_argument("--analytics", action="store_true", help="Show telemetry analytics")
    
    args = parser.parse_args()
    
    # Get token
    token = args.token or os.environ.get("GITHUB_TELEMETRY_TOKEN")
    if not token:
        print("ERROR: GitHub token required")
        print("  --token YOUR_TOKEN or set GITHUB_TELEMETRY_TOKEN environment variable")
        sys.exit(1)
    
    # Create dashboard
    dashboard = TelemetryDashboard(token)
    
    # Execute command
    if args.list_machines:
        dashboard.list_machines()
    elif args.export_machines:
        dashboard.export_machines(args.export_machines)
    elif args.review_incidents:
        dashboard.review_incidents()
    elif args.list_revoked:
        dashboard.list_revoked_tags()
    elif args.revoke_tag:
        dashboard.revoke_tag(args.revoke_tag, args.reason)
    elif args.unrevoke_tag:
        dashboard.unrevoke_tag(args.unrevoke_tag, args.reason)
    elif args.global_kill:
        dashboard.activate_global_kill(args.reason)
    elif args.check_global:
        dashboard.check_global_kill()
    elif args.analytics:
        dashboard.show_analytics()
    else:
        # Default: show all
        dashboard.list_machines()
        dashboard.check_global_kill()
        dashboard.show_analytics()


if __name__ == "__main__":
    main()
