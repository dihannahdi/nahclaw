# MEMORY.md

## Jadwal KKN & Agenda

### Kelas Pengarahan KKN
- **Hari 1**: 14 Maret 2026, 07:00 - 15:00
- **Hari 2**: 15 Maret 2026, 07:00 - 15:00

### Alarm yang Telah Dijadwalkan
1. **14 Maret 04:00** - Alarm sebelum pengarahan hari 1
2. **15 Maret 04:00** - Alarm sebelum pengarahan hari 2
3. **13 Maret 22:00** - Reminder malam sebelum hari 1
4. **14 Maret 00:00** - Reminder tengah malam sebelum hari 1
5. **14 Maret 22:00** - Reminder malam sebelum hari 2
6. **15 Maret 00:00** - Reminder tengah malam sebelum hari 2

### Agenda Lain
- **12 Maret 08:00** - Submit keterangan magang ke SIMASTER

### File Calendar
- File CSV untuk Google Calendar: `kkn_calendar.csv`
- Format: Subject,Start Date,Start Time,End Date,End Time,Description

### Cara Import ke Google Calendar
1. Buka Google Calendar di browser
2. Klik Settings (roda gigi) → Settings
3. Pilih "Import & export" di menu kiri
4. Klik "Select file from your computer" dan pilih `kkn_calendar.csv`
5. Pilih kalender yang diinginkan
6. Klik "Import"

### Catatan
- Semua alarm sudah diatur via cron jobs di OpenClaw
- Alarm akan muncul sebagai systemEvent di Telegram
- Event di calendar sudah private (hanya kamu yang bisa lihat)