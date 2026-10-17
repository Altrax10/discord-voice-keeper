import os
import sys
import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not (TOKEN and GUILD_ID and CHANNEL_ID):
    sys.exit("TOKEN, GUILD_ID, and CHANNEL_ID must be set in .env")

GUILD_ID = int(GUILD_ID)
CHANNEL_ID = int(CHANNEL_ID)
GUILD = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.voice_states = True


class VoiceKeeper(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.target_channel_id = CHANNEL_ID  # None = stay out of voice

    async def setup_hook(self):
        await self.tree.sync(guild=GUILD)
        self.keep_alive.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def ensure_connected(self):
        if self.target_channel_id is None:
            return
        guild = self.get_guild(GUILD_ID)
        channel = guild.get_channel(self.target_channel_id) if guild else None
        if channel is None:
            return

        vc = guild.voice_client
        if vc is None or not vc.is_connected():
            if vc is not None:
                await vc.disconnect(force=True)
            await channel.connect(self_deaf=True)
            print(f"Connected to {channel.name}")
        elif vc.channel.id != channel.id:
            await vc.move_to(channel)
            print(f"Moved to {channel.name}")

    @tasks.loop(seconds=20)
    async def keep_alive(self):
        try:
            await self.ensure_connected()
        except Exception as e:
            print("Connection failed:", e)

    @keep_alive.before_loop
    async def before_keep_alive(self):
        await self.wait_until_ready()


client = VoiceKeeper()


@client.tree.command(name="join", description="Join a voice channel and stay there", guild=GUILD)
@app_commands.describe(channel="Voice channel (leave empty to use the default)")
@app_commands.default_permissions(manage_guild=True)
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel | None = None):
    await interaction.response.defer(ephemeral=True)
    target_id = channel.id if channel else CHANNEL_ID
    client.target_channel_id = target_id
    try:
        await client.ensure_connected()
        await interaction.followup.send(f"Joined <#{target_id}> ✅", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Failed to join: {e}", ephemeral=True)


@client.tree.command(name="leave", description="Leave the voice channel and stop auto-rejoin", guild=GUILD)
@app_commands.default_permissions(manage_guild=True)
async def leave(interaction: discord.Interaction):
    client.target_channel_id = None
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect(force=True)
    await interaction.response.send_message("Left the voice channel 👋", ephemeral=True)


@client.tree.command(name="status", description="Show the bot's voice status", guild=GUILD)
async def status(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_connected():
        msg = f"Connected to <#{vc.channel.id}>, latency {vc.latency * 1000:.0f} ms"
    elif client.target_channel_id is None:
        msg = "Not connected (auto-rejoin is off, use /join)"
    else:
        msg = "Not connected, trying to rejoin..."
    await interaction.response.send_message(msg, ephemeral=True)


client.run(TOKEN)
