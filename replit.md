# Discord Voice Keeper

This is a Python 3.12 console bot, not a web application. Keep the existing
discord.py stack and project structure.

## Configuration

Provide these settings through Replit Secrets (never commit credentials):

- `TOKEN`: the official Discord application's bot token, not a user token.
- `GUILD_ID`: the Discord server ID.
- `CHANNEL_ID`: the target voice channel ID.

Invite the bot to the server with **View Channel** and **Connect** permissions
for the target channel. Enable Discord Developer Mode to copy the IDs.
The existing python-dotenv support also allows local `.env` configuration.

## Running

Dependencies are declared in `requirements.txt` and installed in Replit.
Use the **Discord Voice Keeper** console workflow, which runs:

```sh
python -u bot.py
```

Successful startup logs `Login sebagai ...`; a successful voice connection logs
`Terhubung ke voice channel`. The bot checks its connection every 20 seconds.
There is no browser UI or HTTP port.

The workflow requires all three settings before it can run. Installing
dependencies alone does not verify Discord login or voice connectivity.
