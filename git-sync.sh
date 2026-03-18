#!/bin/bash

# Git sync script for OpenClaw workspace
# This script automatically commits and pushes changes to GitHub
# Can be called manually or via cron

WORKSPACE_DIR="/root/.openclaw/workspace"
LOG_FILE="/root/.openclaw/workspace/git-sync.log"

# Optional: force sync mode (for manual triggers)
FORCE_SYNC="${1:-false}"

echo "=== Git Sync $(date) ===" >> "$LOG_FILE"
echo "Mode: $([ "$FORCE_SYNC" = "force" ] && echo "FORCE" || echo "AUTO")" >> "$LOG_FILE"

cd "$WORKSPACE_DIR" || exit 1

# Check if we have changes in tracked files
CHANGES=$(git status --porcelain 2>/dev/null | grep -E '^(M|A|D|R|C)' || true)
UNTRACKED=$(git status --porcelain 2>/dev/null | grep '^??' || true)

if [ -n "$CHANGES" ] || [ -n "$UNTRACKED" ] || [ "$FORCE_SYNC" = "force" ]; then
    echo "Changes detected or force sync requested:" >> "$LOG_FILE"
    echo "Tracked changes: $([ -n "$CHANGES" ] && echo "YES" || echo "NO")" >> "$LOG_FILE"
    echo "Untracked files: $([ -n "$UNTRACKED" ] && echo "YES" || echo "NO")" >> "$LOG_FILE"
    echo "Force sync: $([ "$FORCE_SYNC" = "force" ] && echo "YES" || echo "NO")" >> "$LOG_FILE"
    
    # Add core files (always track these)
    git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md MEMORY.md .gitignore README.md git-sync.sh
    
    # Add memory files
    if [ -d "memory" ]; then
        git add memory/
    fi
    
    # Add skills (excluding compiled Python files)
    if [ -d "skills" ]; then
        find skills -name "*.pyc" -o -name "__pycache__" -prune -o -type f -print | xargs git add 2>/dev/null || true
    fi
    
    # Check if we actually have something to commit
    if git diff --cached --quiet && [ "$FORCE_SYNC" != "force" ]; then
        echo "No staged changes to commit (only untracked files excluded by .gitignore)" >> "$LOG_FILE"
    else
        # Commit with timestamp
        COMMIT_MSG="Auto-sync: $(date '+%Y-%m-%d %H:%M:%S UTC')"
        if [ "$FORCE_SYNC" = "force" ]; then
            COMMIT_MSG="Manual sync: $(date '+%Y-%m-%d %H:%M:%S UTC')"
        fi
        
        git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
        
        # Try to push (will fail if SSH key not set up yet)
        echo "Attempting push to GitHub..." >> "$LOG_FILE"
        if git push origin main >> "$LOG_FILE" 2>&1; then
            echo "✓ Push successful" >> "$LOG_FILE"
        else
            echo "✗ Push failed (SSH key not configured on GitHub)" >> "$LOG_FILE"
            echo "   Add SSH key to GitHub: Settings → SSH and GPG keys" >> "$LOG_FILE"
            echo "   Public key: $(cat /root/.ssh/id_ed25519.pub)" >> "$LOG_FILE"
        fi
    fi
else
    echo "No changes to commit" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"