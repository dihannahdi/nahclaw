#!/bin/bash

# Git sync script for OpenClaw workspace
# This script automatically commits and pushes changes to GitHub

WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_FILE="/root/.openclaw/workspace/git-sync.log"

echo "=== Git Sync $(date) ===" >> "$LOG_FILE"

cd "$WORKSPACE_DIR" || exit 1

# Check if we have changes
if git status --porcelain | grep -q .; then
    echo "Changes detected, committing..." >> "$LOG_FILE"
    
    # Add core files
    git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md MEMORY.md .gitignore
    
    # Add memory files
    if [ -d "memory" ]; then
        git add memory/
    fi
    
    # Add skills (excluding compiled Python files)
    if [ -d "skills" ]; then
        find skills -name "*.pyc" -o -name "__pycache__" -prune -o -type f -print | xargs git add 2>/dev/null || true
    fi
    
    # Commit with timestamp
    git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    
    # Try to push (will fail if SSH key not set up yet)
    if git push origin main >> "$LOG_FILE" 2>&1; then
        echo "Push successful" >> "$LOG_FILE"
    else
        echo "Push failed (check SSH key setup)" >> "$LOG_FILE"
    fi
else
    echo "No changes to commit" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"