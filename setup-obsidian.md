# Setup Obsidian Sync dengan OpenClaw VPS

## Step 1: Clone Repository di Laptop

```bash
git clone https://github.com/dihannahdi/nahclaw.git
cd nahclaw
```

## Step 2: Buka sebagai Obsidian Vault

1. Buka Obsidian
2. Klik "Open folder as vault"
3. Pilih folder `nahclaw` yang baru di-clone

## Step 3: Setup Git Sync di Laptop

### Option A: Manual Sync
```bash
# Pull updates dari VPS
git pull origin main

# Push changes ke GitHub (jika ada edit di laptop)
git add .
git commit -m "Update dari laptop"
git push origin main
```

### Option B: Auto-sync dengan Git plugin
1. Install plugin "Obsidian Git" di Obsidian
2. Configure settings:
   - Auto pull: Every 10 minutes
   - Auto commit: Every 10 minutes  
   - Auto push: After commit
3. Enable plugin

## Step 4: SSH Key untuk Push dari VPS

Public key dari VPS sudah ada di README.md. Tambahkan ke GitHub:

1. Buka GitHub → Settings → SSH and GPG keys
2. Klik "New SSH key"
3. Title: "OpenClaw VPS"
4. Paste key:
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAM3WFtmIFySjXhGR1/SwtY1NypDr+0et1Bg+x9vNDOB jarvis@openclaw.ai
   ```
5. Save

## Step 5: Test Sync

### Dari VPS:
```bash
cd /root/.openclaw/workspace
./git-sync.sh
cat git-sync.log
```

### Dari Laptop:
```bash
cd ~/nahclaw
git pull
```

## File Structure di Obsidian

- **AGENTS.md** - Konfigurasi AI assistant
- **SOUL.md** - Kepribadian Jarvis
- **MEMORY.md** - Memori utama (jadwal, tugas, catatan)
- **memory/** - File memori harian
- **skills/** - Skill custom untuk OpenClaw

## Tips

1. **Jangan edit file runtime** - File seperti `.gitignore`, script `.sh`, dll sebaiknya diedit di VPS
2. **Memory files otomatis** - File di folder `memory/` dibuat otomatis oleh OpenClaw
3. **Sync terjadwal** - VPS akan auto-commit setiap jam (cron job)
4. **Conflict resolution** - Jika ada conflict, prioritaskan changes dari VPS karena lebih up-to-date

## Troubleshooting

### Push gagal dari VPS:
```bash
# Cek SSH key
ssh -T git@github.com

# Jika "Permission denied", pastikan SSH key sudah ditambahkan ke GitHub
```

### Pull gagal di laptop:
```bash
# Stash changes lokal
git stash
git pull
git stash pop
```

### Obsidian Git plugin error:
- Pastikan Git terinstall di laptop
- Coba manual sync dulu via terminal