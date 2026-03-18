# SKILLS MEMORY

## Available Skills in OpenClaw

### Google Workspace (gog)
- **Skill**: `gog` - Google Workspace CLI untuk Gmail, Calendar, Drive, Contacts, Sheets, Docs
- **Location**: `/usr/lib/node_modules/openclaw/skills/gog/SKILL.md`
- **Status**: Installed and authenticated with `dihannahdii@gmail.com`
- **Commands**:
  - `gog calendar events primary --from YYYY-MM-DD --to YYYY-MM-DD` - Lihat event
  - `gog calendar create primary --summary "Judul" --from YYYY-MM-DDTHH:MM:SS+07:00 --to YYYY-MM-DDTHH:MM:SS+07:00` - Buat event
  - `gog calendar update primary <eventId> --summary "Judul Baru"` - Update event
  - `gog calendar colors` - Lihat warna event

### Trello
- **Skill**: `trello` - Trello CLI untuk manajemen board dan cards via REST API
- **Location**: `/usr/lib/node_modules/openclaw/skills/trello/SKILL.md`
- **Status**: Configured and authenticated
- **Credentials**:
  - API Key: `8727af85864e5522306ba3c902f9bf90`
  - Token: `ATTAa5d9a3da231ec03a1814b912e42df109b5ea7c54df1ffa626ff4eeb0e4502f575EB7EA3B`
  - Secret: `039766c498d9d5a2ab3bd1bcb0296afd7c75dc5bcafd4ad5d1863a0f10504db2`
- **Boards Available**:
  1. **Biotech AI** (id: `693a542fdbff84f74685a375`) - https://trello.com/b/xXH4u9W4/biotech-ai
  2. **Bismillah 1 M Sponsor Berkisah 2026** (id: `69a1ac7f11b8c7b9e630ba26`) - https://trello.com/b/SINu76yJ/bismillah-1-m-sponsor-berkisah-2026
  3. **Nahdi Todos** (id: `693a763589e4ba25a8517344`) - https://trello.com/b/xXNl8aCp/nahdi-todos
  4. **Optyma - Milfar Nahdi's Job Desc** (id: `6947c52e7d0ff8d8c03649cf`) - https://trello.com/b/8296sIGF/optyma-milfar-nahdis-job-desc
- **Commands**:
  - List boards: `curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'`
  - Create card: `curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" -d "idList={listId}" -d "name=Card Title"`

### WhatsApp (wacli)
- **Skill**: `wacli` - WhatsApp CLI untuk kirim pesan dan sync history
- **Location**: `/usr/lib/node_modules/openclaw/skills/wacli/SKILL.md`
- **Status**: Available

### WhatsApp Undone
- **Skill**: `whatsapp-undone` - Track undone tasks dari WhatsApp chats
- **Location**: `~/.openclaw/workspace/skills/whatsapp-undone/SKILL.md`
- **Status**: Available

### Weather
- **Skill**: `weather` - Weather forecasts via wttr.in
- **Location**: `/usr/lib/node_modules/openclaw/skills/weather/SKILL.md`
- **Status**: Available

### Healthcheck
- **Skill**: `healthcheck` - Security hardening dan risk-tolerance config
- **Location**: `/usr/lib/node_modules/openclaw/skills/healthcheck/SKILL.md`
- **Status**: Available

### Skill Creator
- **Skill**: `skill-creator` - Create/update AgentSkills
- **Location**: `/usr/lib/node_modules/openclaw/skills/skill-creator/SKILL.md`
- **Status**: Available

### Tmux
- **Skill**: `tmux` - Remote-control tmux sessions
- **Location**: `/usr/lib/node_modules/openclaw/skills/tmux/SKILL.md`
- **Status**: Available

## Usage Notes
- Sebelum menjawab pertanyaan tentang Google Calendar, Trello, atau WhatsApp, cek skill yang tersedia
- Gunakan `memory_search` untuk mencari informasi tentang skill yang sudah digunakan sebelumnya
- Untuk Google Calendar, gunakan skill `gog` dengan format waktu WIB (+07:00)