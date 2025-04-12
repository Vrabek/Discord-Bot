import discord
import asyncio
import os
import random
from discord.ext import commands, tasks


class JCDentonVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sound_folder = os.path.join(os.path.dirname(__file__), "../jc-voicelines")
        self.join_probability = 0.01  # 1% chance to join a voice channel
        self.random_join_task.start()

    @tasks.loop(seconds=300)
    async def random_join_task(self):
        """Periodically checks for users in voice channels and randomly joins one."""
        for guild in self.bot.guilds:
            # Get all voice channels in the guild that have members
            valid_channels = [channel for channel in guild.voice_channels if len(channel.members) > 0]

            if valid_channels:
                # Randomly select one of the valid channels
                channel = random.choice(valid_channels)

                # Check if the bot should join based on the probability
                if random.random() < self.join_probability:
                    await self.join_and_play(channel)
                    return  # Exit after joining one channel to avoid spamming

    async def join_and_play(self, channel):
        """Joins a voice channel and plays a random sound file."""
        if channel.guild.voice_client:
            print(f"Already connected to a voice channel in {channel.guild.name}.")
            return

        if not channel.permissions_for(channel.guild.me).connect:
            print(f"Cannot connect to {channel.name} due to missing permissions.")
            return

        if not channel.permissions_for(channel.guild.me).speak:
            print(f"Cannot speak in {channel.name} due to missing permissions.")
            return
        
        # Connect to the voice channel
        voice_client = await channel.connect()

        print(f"Connected to {channel.name} in {channel.guild.name}.")
        # Choose a random sound file from the folder
        sound_files = [f for f in os.listdir(self.sound_folder) if f.endswith(".mp3")]
        if not sound_files:
            print("No sound files found in the folder.")
            await voice_client.disconnect()
            return

        random_sound = random.choice(sound_files)
        sound_path = os.path.join(self.sound_folder, random_sound)

        # Play the sound file
        print(f"Playing sound: {random_sound}")
        voice_client.play(discord.FFmpegPCMAudio(sound_path), after=lambda e: print(f"Finished playing: {random_sound}"))

        # Wait for the sound to finish playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Disconnect from the voice channel
        await voice_client.disconnect()

    @random_join_task.before_loop
    async def before_random_join_task(self):
        """Wait until the bot is ready before starting the task."""
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(JCDentonVoice(bot))