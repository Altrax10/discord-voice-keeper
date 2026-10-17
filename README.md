# Discord Voice Keeper

Bot Discord sederhana (Python, discord.py) yang masuk ke satu voice channel dan tetap di sana. Kalau terputus, ter-kick, atau dipindah, bot otomatis masuk lagi.

## Fitur
- Join voice channel tertentu dan stay 24/7
- Auto-reconnect (cek tiap 20 detik)
- Self-deafen supaya hemat bandwidth
- Siap deploy via Docker atau `python bot.py`

## Setup

1. Buat bot di [Discord Developer Portal](https://discord.com/developers/applications), lalu salin token-nya.
2. Invite bot ke server dengan permission **View Channel** dan **Connect**.
3. Aktifkan Developer Mode di Discord untuk menyalin ID server dan ID voice channel.
4. Salin `.env.example` menjadi `.env`, lalu isi:
   ```
   TOKEN=token_bot_kamu
   GUILD_ID=id_server
   CHANNEL_ID=id_voice_channel
   ```

## Menjalankan

```bash
pip install -r requirements.txt
python bot.py
```

### Docker

```bash
docker build -t voice-keeper .
docker run -d --restart unless-stopped --env-file .env voice-keeper
```

### PM2 (VPS)

```bash
pm2 start bot.py --interpreter python3 --name voice-keeper
pm2 save
```

## Catatan
- Gunakan **bot account resmi**. Token akun user (self-bot) melanggar ToS Discord.
- Jangan pernah commit file `.env` atau membagikan token. Kalau token bocor, reset di Developer Portal.
- Sebagian bot timer/leveling tidak menghitung bot, atau baru menghitung kalau ada member manusia di channel.
- Gunakan hanya di server milikmu atau yang sudah mengizinkan.

## Lisensi
MIT
