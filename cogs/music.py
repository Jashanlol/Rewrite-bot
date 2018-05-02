import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
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
    'before_options': '-nostdin',
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

class Reformat:

    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):

        ctx = reaction.message.guild
        if user.id == self.bot.user.id:
            return
        if reaction.emoji == '⏯':
            await reaction.message.remove_reaction(reaction.emoji, user)
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
            elif ctx.voice_client.is_paused():
                ctx.voice_client.resume()
        elif reaction.emoji == '⏹':
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await reaction.message.delete()
        elif reaction.emoji == ''


    @commands.command()
    @commands.guild_only()
    async def play(self, ctx, *, url):

        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        e = discord.Embed(color=ctx.author.color)
        e.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        e.add_field(name='Now playing', value="```py\n{}```".format(player.title))
        e.add_field(name='Song Link', value='{}'.format(url))
        msg = await ctx.send(embed=e)
        reactions = ['⏯','⏹']
        for reaction in reactions:
            await msg.add_reaction(reaction)

    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx):

        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    @commands.command(hidden=True)
    @commands.guild_only()
    async def cleanup(self, ctx):

        discord.AudioSource.cleanup(ctx.voice_client.source)


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(Reformat(bot))