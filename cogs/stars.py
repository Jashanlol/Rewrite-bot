import discord
from discord.ext import commands
import os
import datetime

from .utils.dataIO import dataIO


class StarManager:
    def __init__(self, bot):
        self.bot = bot
        self.starchannel = dataIO.load_json("data/starchannel/starchannel.json")
        self.starmanager = dataIO.load_json("data/starmanager/starmanager.json")

    def save_settings(self):
        dataIO.save_json("data/starchannel/starchannel.json", self.starchannel)
        dataIO.save_json("data/starmanager/starmanager.json", self.starmanager)


    @commands.command()
    async def setupstars(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            await ctx.send('Channel is required.')
        if ctx.author is ctx.guild.owner:
            self.starchannel[(str(ctx.guild.id))] = {'channel_mention': channel.mention, "channel": channel.id}
            self.save_settings()
            await ctx.send('Channel saved.')
        else:
            await ctx.send('Only the server can setup stars channel.')

    @commands.command()
    async def starschannel(self, ctx):
        if str(ctx.guild.id) in self.starchannel:
            await ctx.send('Stars channel is ' + self.starchannel[(str(ctx.guild.id))]["channel_mention"])
        else:
            await ctx.send('Stars channel is not setup. Setup now with `r.setupstars`.')

    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '⭐':
            e = discord.Embed(description=reaction.message.content)
            e.set_author(name=reaction.message.author.name, icon_url=reaction.message.author.avatar_url_as(format=None))
            e.timestamp = datetime.datetime.utcnow()
            channel = self.starchannel[(str(reaction.message.guild.id))][("channel")]
            channel2 = discord.utils.get(reaction.message.guild.channels, id=channel)
            msg = await channel2.send(':star: **' + str(reaction.count) + '** ' +
                                      reaction.message.channel.mention + " ID: " + str(reaction.message.id), embed=e)
            if str(reaction.message.guild.id) in self.starmanager:
                self.starmanager[str(reaction.message.guild.id)]["starred_messages"] = {
                    "original_message_id": (reaction.message.id),
                       "starboard_message_id": (msg.id), "stars": (reaction.count)}
                self.save_settings()
            elif str(reaction.message.guild.id) not in self.starmanager:
                self.starmanager[str(reaction.message.guild.id)] = {
                    "starred_messages":{"original_message_id": (reaction.message.id),
                                           "starboard_message_id": (msg.id), "stars": (reaction.count)}}
                self.save_settings()
            else:
                await reaction.message.channel.send('Stars channel not setup yet. Setup now with `r.setupstars`.')

def check_folders():
    if not os.path.exists("data/starmanager"):
        print("Creating data/starmanager folder...")
        os.makedirs("data/starmanager")

    if not os.path.exists("data/starchannel"):
        print("Creating data/starchannel folder...")
        os.makedirs("data/starchannel")

def check_files():
    if not os.path.exists("data/starmanager/starmanager.json"):
        print("Creating data/starmanager/starmanager.json file...")
        dataIO.save_json("data/starmanager/starmanager.json", {})

    if not os.path.exists("data/starchannel/starchannel.json"):
        print("Creating data/starchannel/starchannel.json file...")
        dataIO.save_json("data/starchannel/starchannel.json", {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(StarManager(bot))
