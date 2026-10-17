import os
import sys
import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not (TOKEN and GUILD_ID and CHANNEL_ID):
    sys.exit("TOKEN, GUILD_ID, dan CHANNEL_ID wajib diisi di file .env")

GUILD_ID = int(GUILD_ID)
CHANNEL_ID = int(CHANNEL_ID)

intents = discord.Intents.default()
intents.voice_states = True


class VoiceKeeper(discord.Client):
    async def setup_hook(self):
        self.keep_alive.start()

    async def on_ready(self):
        print(f"Login sebagai {self.user} (ID: {self.user.id})")

    @tasks.loop(seconds=20)
    async def keep_alive(self):
        guild = self.get_guild(GUILD_ID)
        if guild is None:
            return
        channel = guild.get_channel(CHANNEL_ID)
        if channel is None:
            return

        vc = guild.voice_client
        try:
            if vc is None or not vc.is_connected():
                if vc is not None:
                    await vc.disconnect(force=True)
                await channel.connect(self_deaf=True)
                print("Terhubung ke voice channel")
            elif vc.channel.id != CHANNEL_ID:
                await vc.move_to(channel)
                print("Dipindah kembali ke voice channel yang benar")
        except Exception as e:
            print("Gagal konek:", e)

    @keep_alive.before_loop
    async def before_keep_alive(self):
        await self.wait_until_ready()


client = VoiceKeeper(intents=intents)
client.run(TOKEN)
