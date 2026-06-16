#!/usr/bin/env python3
"""
Purge git history of nawaz1-quantum-software repo.
Creates a single clean commit with current files only.
Removes all historical commits so attackers can't study security implementation.
"""
import subprocess
import os
import sys

REPO_DIR = "c:/Users/IMRAN/.qoder/nawaz1-quantum-software"

def run(cmd, cwd=REPO_DIR):
    """Run a git command and return output."""
    print(f"  Running: {cmd}")
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True
    )
    if result.returncode != 0 and "warning" not in result.stderr.lower():
        print(f"  STDERR: {result.stderr}")
    return result.stdout.strip()

print("=" * 60)
print("GIT HISTORY PURGE — nawaz1-quantum-software")
print("=" * 60)

# Step 1: Get list of tracked files
print("\n[1/6] Getting tracked files...")
files = run("git ls-files").split("\n")
print(f"  Found {len(files)} tracked files")

# Step 2: Create orphan branch
print("\n[2/6] Creating orphan branch...")
run("git checkout --orphan clean_main")
run("git reset")

# Step 3: Re-add all files
print("\n[3/6] Re-adding all files...")
run("git add -A")
status = run("git status --short")
added_count = len([l for l in status.split("\n") if l.strip()])
print(f"  Staged {added_count} files")

# Step 4: Commit as single clean commit
print("\n[4/6] Creating single clean commit...")
commit_msg = "nawaz1 quantum software — Linux x86_64 + ARM64 binaries with full test suite"
run(f'git commit -m "{commit_msg}"')

# Step 5: Replace main branch
print("\n[5/6] Replacing main branch...")
run("git branch -D main")
run("git branch -m clean_main main")

# Step 6: Verify
print("\n[6/6] Verifying...")
log = run("git log --oneline")
print(f"  History: {log}")
file_count = len(run("git ls-files").split("\n"))
print(f"  Files: {file_count}")

print("\n" + "=" * 60)
print("PURGE COMPLETE — single commit, no history")
print("Ready to force push: git push --force origin main")
print("=" * 60)
