import discord
import youtube_dl
from discord.ext import commands
from random import shuffle

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.music_queue = []

        self.is_playing = False

        self.vc = None

        self.loop = False

        self.now_playing = {}


    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    def search_yt(self, item):
        try:
            info = ytdl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
        except Exception:
            return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}


    def play_music(self):
        if len(self.music_queue) > 0 or self.loop:

            self.is_playing = True
            
            if self.loop:
                m_url = self.now_playing['source']

            else:
                self.now_playing = self.music_queue[0]
                m_url = self.now_playing['source']
                self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **ffmpeg_options), after = lambda e: self.play_music())

        else:
            self.is_playing = False
            self.vc = None
            self.now_playing = {}


    @commands.command()
    async def play(self, ctx, *, query):
        """Streams music from an url or searchs from the name"""
        if self.vc == ctx.voice_client or self.vc is None:
            self.vc = ctx.voice_client
            song = self.search_yt(query)
            await ctx.channel.send(f"\"{song['title']}\" added to queue")
            self.music_queue.append(song)

            if self.is_playing == False:
                self.now_playing = self.music_queue[0]
                self.play_music()

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        if volume <= 200:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        self.vc = None
        self.music_queue = []
        self.is_playing = False
        self.loop = False
        self.now_playing = {}

    @commands.command()
    async def queue(self, ctx):
        """Shows the music queue"""
        queue = ""
        for i in range(0, len(self.music_queue)):
            queue += str(i+1) + ". " + self.music_queue[i]['title'] + "\n"

        if queue != "":
            await ctx.channel.send(queue, reference = ctx.message)
        else:
            await ctx.channel.send("The music queue is empty", reference = ctx.message)

    @commands.command()
    async def rm(self, ctx, index : int):
        """Removes a song from the queue"""
        try:
            if len(self.music_queue) >= index:
                await ctx.channel.send(f"Removed \"{self.music_queue[index-1]['title']}\" from the queue", reference = ctx.message)
                del self.music_queue[index-1]
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffles the queue"""
        try:
            if len(self.music_queue) > 0:
                shuffle(self.music_queue)
                await ctx.channel.send("Shuffled the queue", reference = ctx.message)
            else:
                await ctx.channel.send("The music queue is empty", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    async def loop(self, ctx):
        """Loops the current song"""
        try:
            self.loop  = not self.loop
            if self.loop:
                await ctx.channel.send("Loop turned on", reference = ctx.message)
                if self.now_playing != {}:
                    self.loop_song = .insert(0,self.now_playing)
            else:
                await ctx.channel.send("Loop turned off", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    async def now(self, ctx):
        """Shows the current playing song"""
        try:
            if self.now_playing != {}:
                await ctx.channel.send(f"Playing now: \"{self.now_playing['title']}\"", reference = ctx.message)
            else:
                await ctx.channel.send("There is nothing playing", reference = ctx.message)
        except:
            await ctx.channel.send("Exception occured")

    @commands.command()
    async def skip(self, ctx):
        """Skips the current song"""
        if self.vc != "":
            self.vc.pause()
            self.play_music()

    @commands.command()
    async def pause(self, ctx):
        """Pauses the current song"""
        if self.vc != "":
            self.vc.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes the current song"""
        if self.vc != "":
            self.vc.resume()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if self.vc is None:
            if ctx.voice_client is None:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("You are not connected to a voice channel.")
                    raise commands.CommandError("Author not connected to a voice channel.")
            elif ctx.voice_client.is_playing():
                ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))

