# NahClaw - OpenClaw Workspace

This repository contains the workspace configuration for OpenClaw AI assistant running on VPS.

## Structure

- **AGENTS.md** - Core agent configuration and response rules
- **SOUL.md** - Personality and behavior guidelines
- **IDENTITY.md** - Agent identity (Jarvis)
- **USER.md** - Information about the human user (Dihan Nahdi)
- **TOOLS.md** - SSH connections and technical notes
- **HEARTBEAT.md** - Periodic check tasks
- **MEMORY.md** - Main memory file with important information
- **memory/** - Daily memory files (auto-generated)
- **skills/** - Custom skills for OpenClaw

## Current Skills

1. **Bahtsul Masail** - Islamic jurisprudence API integration
2. **Context7** - Documentation search via API
3. **Google Workspace (gog)** - Gmail, Calendar, Drive, etc.
4. **Trello** - Trello board management

## Sync Setup

### VPS → GitHub
- Git repository initialized in `/root/.openclaw/workspace`
- Auto-sync script: `git-sync.sh`
- Cron job runs every hour for automatic commits

### GitHub → Laptop (Obsidian)
1. Clone this repo on your laptop:
   ```bash
   git clone https://github.com/dihannahdi/nahclaw.git
   ```
2. Open the folder as an Obsidian vault
3. Setup Git pull/push for bidirectional sync

## SSH Key Setup (for VPS push)

Public key for VPS:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAM3WFtmIFySjXhGR1/SwtY1NypDr+0et1Bg+x9vNDOB jarvis@openclaw.ai
```

Add this to GitHub → Settings → SSH and GPG keys

## Auto-sync Cron Job

On VPS, runs hourly:
```bash
0 * * * * /root/.openclaw/workspace/git-sync.sh
```

## Notes

- Sensitive files (API keys, credentials) are excluded via `.gitignore`
- Runtime files and temporary data are not synced
- Memory files are updated daily with agent interactions