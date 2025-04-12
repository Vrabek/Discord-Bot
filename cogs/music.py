import discord
import asyncio
import yt_dlp
import discord.ext.commands as commands


class Music(commands.Cog):
    """Music commands for the bot."""
    def __init__(self, bot):

        self.FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -b:a 192k'  # Exclude video and set audio bitrate to 192kbps
        }

        self.YTDL_OPTIONS = {
                        'format': 'bestaudio/best',
                        'noplaylist': True,
                        'quiet': True,
                        'extractaudio': True,
                        'audioformat': 'mp3',        # Convert audio to mp3 format (optional)
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',  # Use mp3 codec for better compatibility
                            'preferredquality': '192',  # Set audio bitrate (e.g., 192kbps)
        }]
        }

        self.bot = bot
        self.ytdl = yt_dlp.YoutubeDL(self.YTDL_OPTIONS)
        self.idle_task = None
        self.queue = {}
               
    async def join(self, ctx):
        """Joins the users voice channel"""
        if ctx.author.voice is None:
            # send direct message to user
            await ctx.author.send(
            "You need to be in a voice channel to play music. " \
            "Join the voice channel and try again.🖕")
            return
        elif ctx.voice_client is None or ctx.voice_client.channel != ctx.author.voice.channel:
            # connect to the voice channel
            await ctx.author.voice.channel.connect()
    @staticmethod
    def _is_valid_url(url_string: str) -> bool:
        """Checks if the URL is valid"""
        return url_string.startswith('https://www.youtube.com/watch?v=') or \
               url_string.startswith('https://youtu.be/') or \
               url_string.startswith('https://www.youtube.com/playlist?list=')


    async def disconnect_if_idle(self, ctx, delay: int = 60):
        """Disconnects the bot if it is not playing after a delay."""
        await asyncio.sleep(delay)
        voice_client = ctx.voice_client
        if voice_client and not voice_client.is_playing():
            await voice_client.disconnect()
            await ctx.send("👋 Left the voice channel due to inactivity.")

        
    @commands.command()
    async def play(self, ctx, *, input_str: str):
        """Adds a song to the queue and starts playing if not already playing."""
        await self.join(ctx)

        # Initialize the queue for the guild if it doesn't exist
        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = []

        # Add the song to the queue
        self.queue[ctx.guild.id].append(input_str)
        await ctx.send(f"🎵 Added to queue: **{input_str}**")

        # Start playing if not already playing
        voice_client = ctx.voice_client
        if not voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        """Plays the next song in the queue."""
        if ctx.guild.id not in self.queue or not self.queue[ctx.guild.id]:
            # If the queue is empty, disconnect after a delay
            self.idle_task = asyncio.create_task(self.disconnect_if_idle(ctx))
            return

        # Get the next song from the queue
        next_song = self.queue[ctx.guild.id].pop(0)
        voice_client = ctx.voice_client

        # Extract audio info
        if self._is_valid_url(next_song):
            info = self.ytdl.extract_info(next_song, download=False)
        else:
            search_query = f"ytsearch1:{next_song}"
            info = self.ytdl.extract_info(search_query, download=False)
            if "entries" in info:
                info = info["entries"][0]

        audio_url = info['url']
        title = info.get('title', 'Unknown Title')

        # Play the audio
        voice_client.play(
            discord.FFmpegPCMAudio(audio_url, **self.FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
        )
        await ctx.send(f"🎶 Now playing: **{title}**")

    @commands.command(alias=['quit'])
    async def leave(self, ctx):
        """Disconnects the bot from the voice channel."""
        if self.idle_task:
            self.idle_task.cancel()
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send("👋 Left the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel!")
    
    @commands.command(alias=['queue','list'])
    async def show_queue(self, ctx):
        """Displays the current queue."""
        if ctx.guild.id not in self.queue or not self.queue[ctx.guild.id]:
            await ctx.send("The queue is empty.")
            return

        queue_list = "\n".join(f"{i + 1}. {song}" for i, song in enumerate(self.queue[ctx.guild.id]))
        await ctx.send(f"🎶 Current queue:\n{queue_list}")

    @commands.command()
    async def skip(self, ctx):
        """Skips the currently playing song."""
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("⏭️ Skipped the current song.")
        else:
            await ctx.send("I'm not playing anything right now.")

async def setup(bot):
    await bot.add_cog(Music(bot))