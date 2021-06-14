import discord
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from random import shuffle

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect(force=True)
        self.vc = None
        self.music_queue = []
        self.is_playing = False
        self.loop = False
        self.now_playing = {}

    @commands.command()
    async def queue(self, ctx):
        """Shows the music queue"""

        added = ""
        i = 1
        j = 1
        k = 1

        embed = discord.Embed(title = f"Song Queue Part {k}")
        
        embed_length = 0

        if len(self.music_queue) > 0:

            for song in self.music_queue:

                to_be_added = str(i) + ". " + song['title'] + "\n"

                if len(added) + len(to_be_added) > 1024:

                    if embed_length + len(added) > 6000:

                        await ctx.channel.send(content=None, embed=embed, reference = ctx.message)
                        embed_length = 0
                        k += 1
                        embed = discord.Embed(title = f"Song Queue Part {k}")

                    embed.add_field(name = f"Songs {j}", value = added)
                    embed_length += len(added)
                    added = to_be_added
                    j += 1

                else:
                    added += to_be_added

                i += 1

            if len(added) > 0:

                if embed_length + len(added) > 6000:

                    await ctx.channel.send(content=None, embed=embed, reference = ctx.message)
                    k += 1
                    embed = discord.Embed(title = f"Song Queue Part {k}")

                embed.add_field(name = f"Songs {j}", value = added)

            await ctx.channel.send(content=None, embed=embed, reference = ctx.message)
            
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
    async def clear(self, ctx):
        """Cleares the music queue"""
        try:
                self.music_queue.clear()
                await ctx.channel.send(f"Cleared the music queue", reference = ctx.message)
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

    @commands.command()
    async def splay(self, ctx, playlist_url):
        """Gets Spotify playlist and searchs on Youtube"""

        results = spotify.user_playlist_tracks(user="",playlist_id=playlist_url)
        track_list = []

        song_number = len(results["items"])
        await ctx.channel.send(f"Adding {song_number} songs to queue, it can take about {song_number} seconds.")

        for i in results["items"]:

            if (i["track"]["artists"].__len__() == 1):

                track_list.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])

            else:
                name_string = ""

                for index, b in enumerate(i["track"]["artists"]):
                    name_string += (b["name"])

                    if (i["track"]["artists"].__len__() - 1 != index):
                        name_string += ", "

                track_list.append(i["track"]["name"] + " - " + name_string)   

        for track in track_list:
            await self.play(ctx=ctx, query=track)

    @commands.command()
    async def skipto(self, ctx, index:int):
        """Skips to the specified song"""
        if self.vc != "":
            self.vc.pause()
            self.music_queue.insert(0, self.music_queue.pop(index-1))
            self.play_music()

    @play.before_invoke
    @splay.before_invoke
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

