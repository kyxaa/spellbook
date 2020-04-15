import youtube_dl
import discord
import asyncio
from discord.ext import commands
#YOUTUBE STUFF

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
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class voiceAudio(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.dndMusic = {
            "forestAmb1":"https://www.youtube.com/watch?v=6Em9tLXbhfo",
            "warAmb":"https://www.youtube.com/watch?v=0rl7AatkjfA",
            "battleMusic":"https://www.youtube.com/watch?v=w0sUw735gRw",
            "battleMusic1":"https://www.youtube.com/watch?v=4szfmKTFoXA",
            "vikingMusic":"https://www.youtube.com/watch?v=tOP07Scqs7I",
            "epicBattle":"https://www.youtube.com/watch?v=M_hrNDhLwvE",
            "rickRoll":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "horseCart":"https://www.youtube.com/watch?v=65TV8jhp9Ns",
            "witcherBattle":"https://www.youtube.com/watch?v=lAGm9MTyRJ8",
            "nightCamp":"https://www.youtube.com/watch?v=7KFoj-SOfHs",
            "quiteForest":"https://www.youtube.com/watch?v=vefCdLtCjyE",
            "dungeonAmb":"https://www.youtube.com/watch?v=wScEFaoqwPM",
            "coldMountain":"https://www.youtube.com/watch?v=mtmB30Prqvs",
            "farmAmb":"https://www.youtube.com/watch?v=BbZ0SMCMdOo",
            "plainsAmb":"https://www.youtube.com/watch?v=q89BgsmHFMc",
            "dampCave":"https://www.youtube.com/watch?v=E72yDpAfrgY",
            "rainAmb":"https://www.youtube.com/watch?v=KSSpVMIgN2Y",
            "townAmb":"https://www.youtube.com/watch?v=NeOg8iCFfTA",
            "fantasyMusic":"https://www.youtube.com/watch?v=4bhceZgdWFM",
            "celticMusic":"https://www.youtube.com/watch?v=b8jyxJaqovk",
            "eerieMusic":"https://www.youtube.com/watch?v=Z6ylGHfLrdI",
            "forestAmb":"https://www.youtube.com/watch?v=xNN7iTA57jM",
            "cataAmb":"https://www.youtube.com/watch?v=WPpVMmTt74Q"
        }


    @commands.command()
    async def showDndMusic(self, ctx):
        if ctx.author.id == 158058710760030219:
            keyList = list(self.dndMusic.keys())
            keyList.sort()
            await ctx.send("\n".join(keyList))

    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voiceClient = voice_client
                            break
                    if not "voiceClient" in locals():
                        voiceClient = await ctx.author.voice.channel.connect()
                else:
                    voiceClient = await ctx.author.voice.channel.connect()
                if url in self.dndMusic:
                    url = self.dndMusic[url]
                source = await YTDLSource.from_url(url)
                if voiceClient.is_playing():
                    voiceClient.stop()
                voiceClient.play(source)
            else:
                await ctx.send("You aren't in a voice channel.")

    @commands.command()
    async def playStream(self, ctx, url):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voiceClient = voice_client
                            break
                    if not "voiceClient" in locals():
                        voiceClient = await ctx.author.voice.channel.connect()
                else:
                    voiceClient = await ctx.author.voice.channel.connect()
                if url in self.dndMusic:
                    url = self.dndMusic[url]
                source = await YTDLSource.from_url(url,stream=True)
                if voiceClient.is_playing():
                    voiceClient.stop()
                voiceClient.play(source)
            else:
                await ctx.send("You aren't in a voice channel.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voiceClient = voice_client
                            break
                    if not "voiceClient" in locals():
                        voiceClient = await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("There isn't anything playing.")
                if voiceClient.is_playing():
                    voiceClient.stop()
                else:
                    await ctx.send("There isn't anything playing.")

            else:
                await ctx.send("You aren't in a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voiceClient = voice_client
                            break
                    if not "voiceClient" in locals():
                        voiceClient = await ctx.author.voice.channel.connect()
                else:
                    await ctx.send("There isn't anything playing.")
                if voiceClient.is_playing():
                    voiceClient.pause()
                else:
                    await ctx.send("There isn't anything playing.")
            else:
                await ctx.send("You aren't in a voice channel.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voiceClient = voice_client
                            break
                    if not "voiceClient" in locals():
                        voiceClient = await ctx.author.voice.channel.connect()
                    if voiceClient.is_paused():
                        voiceClient.resume()
                    else:
                        await ctx.send("There isn't anything playing")
                else:
                    await ctx.send("There isn't anything playing")
            else:
                await ctx.send("You aren't in a voice channel.")

    @commands.command()
    async def volume(self, ctx, volume):
        if ctx.author.id == 158058710760030219:
            if hasattr(ctx.author.voice,"channel"):
                if not ctx._state.voice_clients == []:
                    for voice_client in ctx._state.voice_clients:
                        if voice_client.channel == ctx.author.voice.channel:
                            voice_client.source.volume = int(volume)/100
                            break
                else:
                    await ctx.send("There isn't anything playing")
            else:
                await ctx.send("You aren't in a voice channel.")

def setup(bot):
    bot.add_cog(voiceAudio(bot))