# Bahtsul Masail Skill

Skill untuk integrasi dengan API bahtsulmasail.tech - menyediakan jawaban otoritatif untuk pertanyaan fikih Islam dengan referensi dari 7,800+ kitab kuning.

## Fitur Utama

1. **Auto-detection**: Deteksi otomatis pertanyaan Islami berdasarkan keyword
2. **Multi-handler**: Tiga handler dengan optimasi berbeda:
   - `telegram_handler.py` - Optimized for Telegram (8s + 5s fallback)
   - `fast_handler.py` - Ultra-fast (<1s, no AI)
   - `handler.py` - Full-featured (15s timeout)
3. **Ibaroh Support**: Menampilkan teks Arab lengkap dari kitab asli
4. **Fallback Handling**: Graceful degradation saat AI synthesis timeout
5. **API Key Management**: Support untuk environment variable dan config file

## Format Respons

Setiap respons Bahtsul Masail sekarang menyertakan:

### 1. Jawaban AI (jika tersedia)
```
🤖 **Jawaban AI:** [sintesis AI dari referensi kitab]
```

### 2. Referensi Kitab
```
📚 **Referensi (2):**

1. [Judul Kitab]
   📖 [Nama Kitab]
   ✍️ [Pengarang]
   🕌 [Mazhab] (jika ada)
   📄 Halaman: [nomor halaman]
   📝 [Ringkasan isi]
```

### 3. 📜 Ibaroh (Teks Arab Lengkap) - **FITUR BARU**
```
   📜 **Ibaroh (Teks Arab Lengkap):**
      [teks Arab lengkap dari kitab asli]
      [dilanjutkan...]
      ... (selengkapnya di halaman [nomor])
```

### 4. Istilah Arab
```
🔤 **Istilah Arab:** [istilah-istilah Arab yang diterjemahkan]
```

### 5. Informasi Bahasa
```
🌐 **Bahasa:** [bahasa terdeteksi] | **Domain:** [domain fikih]
```

## Cara Penggunaan

### 1. Auto-detection (Default)
```bash
# Tanyakan pertanyaan Islami
"hukum shalat jamak qasar"
"apa hukum batal puasa"
"bagaimana tata cara wudhu"
```

### 2. Manual Command
```bash
# Gunakan command !bahtsul
!bahtsul hukum riba dalam jual beli
!bahtsul syarat sah nikah
```

### 3. Script Langsung
```bash
python3 simple_search.py "hukum puasa ramadhan"
python3 telegram_handler.py "hukum shalat jumat"
python3 fast_handler.py "hukum zakat fitrah"
```

## Handler Perbandingan

| Handler | Timeout | AI Synthesis | Ibaroh | Use Case |
|---------|---------|--------------|--------|----------|
| `telegram_handler.py` | 8s + 5s fallback | ✅ (with fallback) | ✅ Lengkap | Telegram integration |
| `fast_handler.py` | <1s | ❌ | ✅ Preview | Fast responses |
| `handler.py` | 15s | ✅ | ✅ Lengkap | Full-featured |
| `simple_search.py` | 30s | ❌ | ✅ Lengkap | Simple reference only |

## Konfigurasi API Key

### 1. Environment Variable (Recommended)
```bash
export BAHTSUL_API_KEY="bm_29b2bae43d194501ade693333863a996"
```

### 2. OpenClaw Configuration
```json
{
  "env": {
    "vars": {
      "BAHTSUL_API_KEY": "bm_29b2bae43d194501ade693333863a996"
    }
  }
}
```

### 3. Hardcoded (Fallback)
```python
API_KEY = "bm_29b2bae43d194501ade693333863a996"
```

## Islamic Keywords untuk Auto-detection

```
shalat, salat, sholat, puasa, zakat, nikah, talak, riba, haji, umrah, wudhu, 
tayammum, janabah, haid, nifas, mazhab, fiqh, fikih, kitab, kuning, arab, 
islam, quran, hadis, hadith, sunnah, makruh, haram, halal, wajib, sunnah, 
mubah, makruh, haram, murtad, kafir, muslim, muslimah, jilbab, hijab, aurat, 
mahram, muhrim, waris, warisan, faraid, wasiat, wakaf, sedekah, infaq, jumat, 
jumuah, jamaah, imam, makmum, masjid, musholla, azan, adzan, iqamah, iqomat, 
sholat jumat, sholat jenazah, sholat id, idul fitri, idul adha, qurban, 
udhiyah, aqiqah, khitan, sunat, khulu, li'an, iddah, mutah, muhrim, khalwat, 
ikhtilat, aurat, tabarruj, ghibah, fitnah
```

## Backend Service

- **Service**: `kizana-backend`
- **Port**: 8080
- **Endpoint**: `POST http://127.0.0.1:8080/api/v1/search`
- **Auth**: `X-API-Key` header
- **Management**: `systemctl restart kizana-backend`

## Troubleshooting

### 1. API Timeout
```bash
# Cek status backend
systemctl status kizana-backend

# Restart jika perlu
systemctl restart kizana-backend
```

### 2. Invalid API Key
```bash
# Verifikasi key
echo $BAHTSUL_API_KEY

# Test dengan curl
curl -X POST http://127.0.0.1:8080/api/v1/search \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $BAHTSUL_API_KEY" \
  -d '{"query": "test", "max_results": 1, "include_ai": false}'
```

### 3. Response terlalu panjang untuk Telegram
- Gunakan `fast_handler.py` untuk preview
- Handler otomatis memotong teks Arab yang terlalu panjang
- Ibaroh ditampilkan dalam chunks yang manageable

## Contoh Respons Lengkap

```
🔍 **Bahtsul Masail Search**
**Query:** hukum batal puasa

🤖 **Jawaban AI:** Puasa batal karena makan/minum dengan sengaja, hubungan intim, muntah dengan sengaja, haid/nifas, dan berlebih-lebihan dalam berkumur.

📚 **Referensi (2):**

1. **ما يبطل الصوم** (Apa yang Membatalkan Puasa)
   📖 Kitab Fiqh
   ✍️ صهيب عبد الجبار
   🕌 Syafi'i
   📄 Halaman: 271
   📝 Makan/minum dengan sengaja membatalkan puasa. Hadits Abu Hurairah RA tentang makan/minum karena lupa. Berlebih-lebihan dalam berkumur dan istinsyaq. Muntah dengan sengaja.

   📜 **Ibaroh (Teks Arab Lengkap):**
      مما يبطل الصوم: الأكل والشرب عمداً، والجماع، والاستقاء عمداً، والحَيْض والنِّفاس، والغُلُو في المضمضة والاستنشاق حتى يصل الماء إلى الحلق.
      ... (selengkapnya di halaman 271)

2. **مبطلات الصيام** (Pembatal-pembatal Puasa)
   📖 الجهاد في سبيل الله تعالى
   ✍️ غير معروف
   📄 Halaman: 10
   📝 Makan dan minum di siang hari (kecuali lupa). Hubungan intim (jima') dengan konsekuensi qadha dan kafarat. Muntah dengan sengaja.

   📜 **Ibaroh (Teks Arab Lengkap):**
      مبطلات الصيام: الأكل والشرب نهاراً إلا النسيان، والجماع وعليه القضاء والكفارة، والاستقاء عمداً.
      ... (selengkapnya di halaman 10)

🔤 **Istilah Arab:** صوم, فطر, قضاء, كفارة, جماع, استقاء

🌐 **Bahasa:** id | **Domain:** fiqh
```

## Changelog

### v1.1.0 (2026-03-14)
- **Fitur Baru**: Ibaroh (teks Arab lengkap) dalam semua respons
- **Enhancement**: Format respons yang lebih terstruktur
- **Optimization**: Chunking teks Arab untuk readability
- **Documentation**: README lengkap dengan contoh

### v1.0.0 (2026-03-14)
- Initial release
- Auto-detection Islamic keywords
- Three handler variants
- API key management
- Fallback handling

## Kontribusi

1. Fork repository
2. Buat branch fitur: `git checkout -b feature/ibaroh-support`
3. Commit changes: `git commit -am 'Add ibaroh support'`
4. Push ke branch: `git push origin feature/ibaroh-support`
5. Buat Pull Request

## Lisensi

Skill ini terintegrasi dengan API bahtsulmasail.tech. Pastikan memiliki API key yang valid dari dihannahdii@gmail.com.

## Kontak

- **API Owner**: dihannahdii@gmail.com
- **Skill Maintainer**: OpenClaw Agent
- **Backend**: kizana-backend service on port 8080